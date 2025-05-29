import tkinter as tk
from tkinter import ttk, Canvas
import psutil
import time
from threading import Thread


class NetworkMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("网速监控工具")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        # 初始化网络计数器
        self.old_download = psutil.net_io_counters().bytes_recv
        self.old_upload = psutil.net_io_counters().bytes_sent

        # 创建界面组件
        self.create_widgets()
        # 启动实时更新线程
        self.update_thread = Thread(target=self.update_metrics, daemon=True)
        self.update_thread.start()

    def create_widgets(self):
        # 顶部标题
        tk.Label(self.root, text="实时网速监控", font=("微软雅黑", 16, "bold")).pack(pady=10)

        # 速度显示框架
        speed_frame = ttk.Frame(self.root)
        speed_frame.pack(pady=20, padx=20, fill="x")

        # 下载速度
        self.download_label = ttk.Label(speed_frame, text="下载速度：0.00 KB/s", font=("微软雅黑", 12))
        self.download_label.pack(side="left", padx=10)

        # 上传速度
        self.upload_label = ttk.Label(speed_frame, text="上传速度：0.00 KB/s", font=("微软雅黑", 12))
        self.upload_label.pack(side="left", padx=10)

        # 图表区域
        self.canvas = Canvas(self.root, width=550, height=150, bg="white")
        self.canvas.pack(pady=10, padx=20)
        self.canvas.create_text(275, 130, text="近10秒网速趋势", font=("微软雅黑", 10))

        # 初始化图表数据
        self.download_history = [0] * 10
        self.upload_history = [0] * 10
        self.plot_graph()

    def get_current_speed(self):
        # 获取当前网络流量
        now = psutil.net_io_counters()
        download = now.bytes_recv
        upload = now.bytes_sent

        # 计算速度（KB/s）
        dl_speed = (download - self.old_download) / 1024
        ul_speed = (upload - self.old_upload) / 1024

        # 更新计数器
        self.old_download = download
        self.old_upload = upload

        return dl_speed, ul_speed

    def update_metrics(self):
        while True:
            dl, ul = self.get_current_speed()
            # 更新标签显示（保留两位小数）
            self.download_label.config(text=f"下载速度：{dl:.2f} KB/s")
            self.upload_label.config(text=f"上传速度：{ul:.2f} KB/s")

            # 更新历史数据
            self.download_history.pop(0)
            self.download_history.append(dl)
            self.upload_history.pop(0)
            self.upload_history.append(ul)

            # 刷新图表
            self.root.after(1000, self.plot_graph)  # 每秒更新一次
            time.sleep(1)

    def plot_graph(self):
        self.canvas.delete("all")  # 清空画布
        self.canvas.create_text(275, 130, text="近10秒网速趋势（KB/s）", font=("微软雅黑", 10))

        # 绘制下载速度曲线
        x_start = 30
        y_base = 120
        scale_y = 2  # 纵向缩放比例（可调整曲线高度）
        for i in range(10):
            x1 = x_start + i * 50
            y1 = y_base - self.download_history[i] / scale_y
            x2 = x_start + (i + 1) * 50
            y2 = y_base - self.download_history[i + 1] / scale_y if i < 9 else y1
            self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=2, tags="download")

        # 绘制上传速度曲线
        for i in range(10):
            x1 = x_start + i * 50
            y1 = y_base + self.upload_history[i] / scale_y
            x2 = x_start + (i + 1) * 50
            y2 = y_base + self.upload_history[i + 1] / scale_y if i < 9 else y1
            self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2, tags="upload")

        # 添加坐标轴标签
        self.canvas.create_text(x_start - 10, y_base, text="0", anchor="e", font=("微软雅黑", 8))
        self.canvas.create_text(x_start + 450, y_base, text="时间（秒）", font=("微软雅黑", 8))
        self.canvas.create_line(x_start, y_base, x_start + 450, y_base, fill="black")  # 时间轴


if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkMonitor(root)
    root.mainloop()