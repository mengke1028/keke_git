import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import time
import threading
import pyautogui
import logging
from datetime import datetime


class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        logging.Handler.__init__(self)
        self.text_widget = text_widget
        self.text_widget.config(state='disabled')

    def emit(self, record):
        msg = self.format(record) + "\n"

        def append():
            self.text_widget.config(state='normal')
            self.text_widget.insert(tk.END, msg)
            self.text_widget.see(tk.END)
            self.text_widget.config(state='disabled')

        self.text_widget.after(0, append)


class RefreshApp:
    def __init__(self, root):
        self.root = root
        self.root.title("网页自动刷新工具")
        self.root.geometry("500x650")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f0f0")

        self.is_running = False
        self.refresh_thread = None
        self.stop_event = threading.Event()

        self.setup_ui()
        self.setup_logger()

    def setup_ui(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 间隔设置部分
        interval_frame = ttk.LabelFrame(main_frame, text="刷新间隔设置", padding="10")
        interval_frame.pack(fill=tk.X, pady=5)

        ttk.Label(interval_frame, text="刷新间隔 (分钟):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.interval_var = tk.DoubleVar(value=5.0)
        interval_spinbox = ttk.Spinbox(interval_frame, from_=0.1, to=60.0, increment=0.5,
                                       textvariable=self.interval_var, width=8)
        interval_spinbox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # 操作按钮部分
        button_frame = ttk.Frame(main_frame, padding="10")
        button_frame.pack(fill=tk.X, pady=5)

        self.start_button = ttk.Button(button_frame, text="开始刷新", command=self.start_refresh)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(button_frame, text="停止刷新", command=self.stop_refresh, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.quit_button = ttk.Button(button_frame, text="退出", command=self.quit_app)
        self.quit_button.pack(side=tk.RIGHT, padx=5)

        # 状态显示部分
        status_frame = ttk.LabelFrame(main_frame, text="刷新状态", padding="10")
        status_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(status_frame, textvariable=self.status_var).pack(anchor=tk.W, pady=5)

        # 日志显示部分
        log_frame = ttk.LabelFrame(main_frame, text="操作日志", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, width=50, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def setup_logger(self):
        self.logger = logging.getLogger("RefreshLogger")
        self.logger.setLevel(logging.INFO)

        # 添加文本控件处理器
        text_handler = TextHandler(self.log_text)
        text_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(text_handler)

    def start_refresh(self):
        # 在单独线程中处理开始逻辑
        threading.Thread(target=self._start_refresh_thread, daemon=True).start()

    def _start_refresh_thread(self):
        # 更新UI状态（通过主线程）
        self.root.after(0, self._update_ui_for_start)

        interval = self.interval_var.get()
        if interval <= 0:
            self.root.after(0, lambda: messagebox.showerror("错误", "刷新间隔必须大于0"))
            self.root.after(0, self._update_ui_for_error)
            return

        self.is_running = True
        self.stop_event.clear()

        self.logger.info(f"开始刷新，间隔: {interval} 分钟")
        self.logger.info("请确保浏览器窗口处于活动状态")

        # 倒计时5秒
        for i in range(5, 0, -1):
            self.root.after(0, lambda i=i: self.status_var.set(f"倒计时: {i} 秒"))
            self.logger.info(f"倒计时: {i} 秒")
            if self.stop_event.is_set():
                self.root.after(0, self._update_ui_for_stop)
                return
            time.sleep(1)

        self.logger.info("开始循环刷新")

        # 启动刷新线程
        # self.refresh_thread = threading.Thread(target=self.refresh_loop, args=(interval,))
        # self.refresh_thread.daemon = True
        # self.refresh_thread.start()
        self.refresh_loop(interval)

    def _update_ui_for_start(self):
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

    def _update_ui_for_error(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_var.set("就绪")

    def _update_ui_for_stop(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_var.set("就绪")

    def stop_refresh(self):
        if not self.is_running:
            return

        self.is_running = False
        self.stop_event.set()

        self.root.after(0, self._update_ui_for_stop)
        self.logger.info("正在停止刷新...")

    def refresh_loop(self, interval):
        try:
            while True:
                try:
                    if not self.stop_event.is_set():
                        pyautogui.press('1')
                        time.sleep(interval * 60)
                        self.logger.info("已按下F5")
                    else:
                        return
                    print(self.stop_event.is_set())
                except:
                    pass

        except Exception as e:
            self.logger.error(f"刷新过程中出错: {str(e)}")
        finally:
            # 确保线程结束时更新UI状态
            self.root.after(0, self._update_ui_for_stop)

    def quit_app(self):
        self.stop_refresh()
        self.root.after(500, self.root.destroy)


if __name__ == "__main__":
    root = tk.Tk()
    app = RefreshApp(root)
    root.mainloop()    