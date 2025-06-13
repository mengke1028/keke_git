import tkinter as tk
from tkinter import ttk
import psutil
import time
from threading import Thread


class NetworkMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("网速监控工具")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # 存储网卡信息
        self.interfaces = self.get_network_interfaces()
        self.selected_interface = tk.StringVar(value=list(self.interfaces.keys())[0])

        # 网络计数器
        self.old_download = 0
        self.old_upload = 0

        # 创建界面
        self.create_widgets()

        # 启动监控线程
        self.is_running = True
        self.monitor_thread = Thread(target=self.monitor_network, daemon=True)
        self.monitor_thread.start()

        # 窗口关闭时停止监控
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def get_network_interfaces(self):
        """获取所有可用的网络接口"""
        interfaces = psutil.net_if_addrs()
        return {name: info for name, info in interfaces.items() if info}

    def create_widgets(self):
        # 标题
        title_label = tk.Label(
            self.root,
            text="网速监控工具",
            font=("微软雅黑", 16, "bold"),
            pady=10
        )
        title_label.pack()

        # 网卡选择下拉框
        interface_frame = ttk.Frame(self.root)
        interface_frame.pack(fill="x", padx=20, pady=10)

        ttk.Label(interface_frame, text="选择网卡:").pack(side="left", padx=5)

        interface_combo = ttk.Combobox(
            interface_frame,
            textvariable=self.selected_interface,
            values=list(self.interfaces.keys()),
            state="readonly",
            width=20
        )
        interface_combo.pack(side="left", padx=5)
        interface_combo.bind("<<ComboboxSelected>>", self.reset_counters)

        # 网速显示区域
        speed_frame = ttk.LabelFrame(self.root, text="实时网速")
        speed_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.download_label = tk.Label(
            speed_frame,
            text="下载: 0.00 KB/s",
            font=("微软雅黑", 14),
            pady=10
        )
        self.download_label.pack()

        self.upload_label = tk.Label(
            speed_frame,
            text="上传: 0.00 KB/s",
            font=("微软雅黑", 14)
        )
        self.upload_label.pack()

        # 状态栏
        self.status_var = tk.StringVar(value="监控中: " + self.selected_interface.get())
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief="sunken",
            anchor="w"
        )
        status_bar.pack(side="bottom", fill="x")

    def reset_counters(self, event=None):
        """切换网卡时重置计数器"""
        self.old_download = self.get_current_bytes()[0]
        self.old_upload = self.get_current_bytes()[1]
        self.status_var.set("监控中: " + self.selected_interface.get())

    def get_current_bytes(self):
        """获取当前网卡的接收和发送字节数"""
        try:
            interface = self.selected_interface.get()
            counters = psutil.net_io_counters(pernic=True)[interface]
            return counters.bytes_recv, counters.bytes_sent
        except (KeyError, AttributeError):
            # 处理网卡不存在的情况
            return 0, 0

    def monitor_network(self):
        """监控网络速度的线程函数"""
        self.reset_counters()

        while self.is_running:
            try:
                # 获取当前字节数
                current_download, current_upload = self.get_current_bytes()

                # 计算速度 (KB/s)
                download_speed = (current_download - self.old_download) / 1024
                upload_speed = (current_upload - self.old_upload) / 1024

                # 更新UI
                self.root.after(0, self.update_speed_labels, download_speed, upload_speed)

                # 更新计数器
                self.old_download = current_download
                self.old_upload = current_upload

                # 等待1秒
                time.sleep(1)
            except Exception as e:
                self.status_var.set(f"错误: {str(e)}")
                time.sleep(1)

    def update_speed_labels(self, download_speed, upload_speed):
        """更新速度标签显示"""
        self.download_label.config(text=f"下载: {download_speed:.2f} KB/s")
        self.upload_label.config(text=f"上传: {upload_speed:.2f} KB/s")

    def on_close(self):
        """窗口关闭时的处理"""
        self.is_running = False
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkMonitor(root)
    root.mainloop()