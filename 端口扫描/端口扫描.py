import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import socket
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed


class PortScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("高效端口扫描器")
        self.root.geometry("650x500")
        self.root.resizable(False, False)

        # 控制扫描状态
        self.is_scanning = False
        # 存储开放的端口
        self.open_ports = []
        # 线程池最大线程数（可根据需要调整，建议100-500）
        self.max_threads = 200

        # 创建UI组件
        self._create_widgets()

    def _create_widgets(self):
        # 1. 输入区域
        input_frame = ttk.LabelFrame(self.root, text="扫描设置")
        input_frame.pack(padx=10, pady=10, fill=tk.X)

        # IP输入
        ttk.Label(input_frame, text="目标IP:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.ip_entry = ttk.Entry(input_frame, width=20)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)
        self.ip_entry.insert(0, "127.0.0.1")

        # 端口范围输入
        ttk.Label(input_frame, text="端口范围:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.port_start = ttk.Entry(input_frame, width=8)
        self.port_start.grid(row=0, column=3, padx=5, pady=5)
        self.port_start.insert(0, "1")

        ttk.Label(input_frame, text="-").grid(row=0, column=4, padx=0, pady=5)

        self.port_end = ttk.Entry(input_frame, width=8)
        self.port_end.grid(row=0, column=5, padx=5, pady=5)
        self.port_end.insert(0, "1000")

        # 超时时间
        ttk.Label(input_frame, text="超时(秒):").grid(row=0, column=6, padx=5, pady=5, sticky=tk.W)
        self.timeout_entry = ttk.Entry(input_frame, width=5)
        self.timeout_entry.grid(row=0, column=7, padx=5, pady=5)
        self.timeout_entry.insert(0, "0.5")  # 缩短超时时间提升速度

        # 线程数设置
        ttk.Label(input_frame, text="线程数:").grid(row=0, column=8, padx=5, pady=5, sticky=tk.W)
        self.thread_entry = ttk.Entry(input_frame, width=5)
        self.thread_entry.grid(row=0, column=9, padx=5, pady=5)
        self.thread_entry.insert(0, "200")

        # 2. 按钮区域
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(padx=10, pady=5, fill=tk.X)

        self.start_btn = ttk.Button(btn_frame, text="开始扫描", command=self.start_scan)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = ttk.Button(btn_frame, text="停止扫描", command=self.stop_scan, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        self.clear_btn = ttk.Button(btn_frame, text="清空结果", command=self.clear_result)
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        # 3. 结果显示区域
        result_frame = ttk.LabelFrame(self.root, text="扫描结果")
        result_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, font=("Consolas", 9))
        self.result_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.result_text.config(state=tk.DISABLED)

    def _log(self, message, color="black"):
        """向结果区域输出日志，支持颜色"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, message + "\n")
        self.result_text.tag_add(color, f"end-{len(message) + 2}c", f"end-1c")
        self.result_text.tag_config("green", foreground="green", font=("Consolas", 9, "bold"))
        self.result_text.tag_config("red", foreground="red")
        self.result_text.tag_config("blue", foreground="blue")
        self.result_text.tag_config("purple", foreground="purple", font=("Consolas", 9, "bold"))
        self.result_text.see(tk.END)
        self.result_text.config(state=tk.DISABLED)

    def _validate_input(self):
        """验证输入是否合法"""
        # 检查IP
        ip = self.ip_entry.get().strip()
        if not ip:
            messagebox.showerror("错误", "请输入目标IP！")
            return None

        # 检查端口范围
        try:
            start = int(self.port_start.get().strip())
            end = int(self.port_end.get().strip())
            if start < 1 or end > 65535 or start > end:
                raise ValueError
        except ValueError:
            messagebox.showerror("错误", "端口范围必须是1-65535之间的数字，且起始≤结束！")
            return None

        # 检查超时时间
        try:
            timeout = float(self.timeout_entry.get().strip())
            if timeout <= 0 or timeout > 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("错误", "超时时间必须是0-10之间的数字！")
            return None

        # 检查线程数
        try:
            threads = int(self.thread_entry.get().strip())
            if threads < 1 or threads > 1000:
                raise ValueError
            self.max_threads = threads
        except ValueError:
            messagebox.showerror("错误", "线程数必须是1-1000之间的整数！")
            return None

        return (ip, start, end, timeout)

    def _scan_port(self, ip, port, timeout):
        """扫描单个端口"""
        if not self.is_scanning:
            return
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            if result == 0:
                self._log(f"[+] {ip}:{port} 开放", "green")
                self.open_ports.append(port)  # 记录开放的端口
            sock.close()
        except Exception:
            pass  # 忽略扫描错误，提升速度

    def start_scan(self):
        """多线程批量扫描端口"""
        # 验证输入
        input_data = self._validate_input()
        if not input_data:
            return

        ip, start, end, timeout = input_data

        # 初始化状态
        self.is_scanning = True
        self.open_ports = []  # 清空历史开放端口
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)

        # 清空结果
        self.clear_result()
        self._log(f"开始多线程扫描 {ip} 的端口 {start}-{end} (线程数:{self.max_threads}，超时{timeout}秒)...", "blue")

        # 多线程扫描核心逻辑
        def scan_thread():
            # 创建线程池
            with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                # 提交所有端口扫描任务
                futures = [executor.submit(self._scan_port, ip, port, timeout)
                           for port in range(start, end + 1)]

                # 监控扫描状态，支持停止
                for future in as_completed(futures):
                    if not self.is_scanning:
                        # 取消未完成的任务
                        for f in futures:
                            f.cancel()
                        break

            # 扫描结束处理
            self.is_scanning = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)

            # 汇总开放端口
            self._log("\n========== 扫描结果汇总 ==========", "blue")
            if self.open_ports:
                self.open_ports.sort()  # 排序开放端口
                open_ports_str = ", ".join(map(str, self.open_ports))
                self._log(f"✅ 开放的端口列表: {open_ports_str}", "purple")
                self._log(f"📊 共发现 {len(self.open_ports)} 个开放端口", "purple")
            else:
                self._log("❌ 未发现任何开放端口", "red")
            self._log("====================================\n", "blue")

        # 启动扫描主线程
        threading.Thread(target=scan_thread, daemon=True).start()

    def stop_scan(self):
        """停止扫描"""
        self.is_scanning = False
        self._log("\n⚠️ 用户手动停止扫描！", "blue")

    def clear_result(self):
        """清空结果区域"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = PortScannerGUI(root)
    root.mainloop()