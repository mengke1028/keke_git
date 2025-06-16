import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext
import threading
import queue
from pdf2docx import Converter
from PyPDF2 import PdfReader
import time


class PDFToWordConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF转Word工具")
        self.root.geometry("800x600")
        self.root.minsize(600, 500)
        self.root.configure(bg="#f5f7fa")

        # 设置中文字体
        self.font_config()

        # 创建任务队列和结果队列
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()

        # 创建UI
        self.create_widgets()

        # 启动处理线程
        self.processing_thread = threading.Thread(target=self.process_tasks, daemon=True)
        self.processing_thread.start()

        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def font_config(self):
        """配置字体以确保中文显示正常"""
        # 显式导入font模块
        import tkinter.font as font

        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="SimHei", size=10)
        self.root.option_add("*Font", default_font)

    def create_widgets(self):
        """创建应用程序界面"""
        # 顶部标题
        header_frame = tk.Frame(self.root, bg="#165DFF", height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(0)

        title_label = tk.Label(header_frame, text="PDF转Word工具",
                               font=("SimHei", 16, "bold"),
                               bg="#165DFF", fg="white")
        title_label.pack(pady=15)

        # 主内容区域
        main_frame = tk.Frame(self.root, bg="#f5f7fa")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 左侧面板 - 文件选择和设置
        left_frame = tk.LabelFrame(main_frame, text="文件设置", bg="#f5f7fa", padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # PDF文件选择
        pdf_frame = tk.Frame(left_frame, bg="#f5f7fa")
        pdf_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(pdf_frame, text="PDF文件:", bg="#f5f7fa").pack(side=tk.LEFT, padx=(0, 10))

        self.pdf_path_var = tk.StringVar()
        pdf_entry = tk.Entry(pdf_frame, textvariable=self.pdf_path_var, width=40)
        pdf_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        browse_btn = tk.Button(pdf_frame, text="浏览...", command=self.browse_pdf,
                               bg="#e0e7ff", fg="#4f46e5", relief=tk.FLAT,
                               padx=10, pady=2)
        browse_btn.pack(side=tk.LEFT, padx=(10, 0))

        # Word文件保存位置
        word_frame = tk.Frame(left_frame, bg="#f5f7fa")
        word_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(word_frame, text="Word文件:", bg="#f5f7fa").pack(side=tk.LEFT, padx=(0, 10))

        self.word_path_var = tk.StringVar()
        word_entry = tk.Entry(word_frame, textvariable=self.word_path_var, width=40)
        word_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        browse_word_btn = tk.Button(word_frame, text="浏览...", command=self.browse_word,
                                    bg="#e0e7ff", fg="#4f46e5", relief=tk.FLAT,
                                    padx=10, pady=2)
        browse_word_btn.pack(side=tk.LEFT, padx=(10, 0))

        # 批量处理选项
        batch_frame = tk.Frame(left_frame, bg="#f5f7fa")
        batch_frame.pack(fill=tk.X, pady=(0, 10))

        self.batch_var = tk.BooleanVar()
        batch_check = tk.Checkbutton(batch_frame, text="批量处理文件夹中的所有PDF",
                                     variable=self.batch_var, command=self.toggle_batch,
                                     bg="#f5f7fa")
        batch_check.pack(anchor=tk.W)

        self.folder_path_var = tk.StringVar()
        folder_entry = tk.Entry(batch_frame, textvariable=self.folder_path_var, width=40, state=tk.DISABLED)
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=5)

        browse_folder_btn = tk.Button(batch_frame, text="浏览...", command=self.browse_folder,
                                      bg="#e0e7ff", fg="#4f46e5", relief=tk.FLAT,
                                      padx=10, pady=2, state=tk.DISABLED)
        browse_folder_btn.pack(side=tk.LEFT, padx=(10, 0))

        # 转换按钮
        convert_btn = tk.Button(left_frame, text="开始转换", command=self.start_conversion,
                                bg="#165DFF", fg="white", font=("SimHei", 12, "bold"),
                                relief=tk.FLAT, padx=20, pady=8, cursor="hand2")
        convert_btn.pack(pady=20)

        # 右侧面板 - 进度和日志
        right_frame = tk.LabelFrame(main_frame, text="转换进度", bg="#f5f7fa", padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # 进度条
        self.progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(right_frame, variable=self.progress_var, length=100, mode='determinate')
        progress_bar.pack(fill=tk.X, pady=(0, 10))

        # 状态标签
        self.status_var = tk.StringVar(value="就绪")
        status_label = tk.Label(right_frame, textvariable=self.status_var, bg="#f5f7fa", fg="#4b5563")
        status_label.pack(anchor=tk.W, pady=(0, 10))

        # 日志区域
        log_frame = tk.LabelFrame(right_frame, text="转换日志", bg="#f5f7fa", padx=5, pady=5)
        log_frame.pack(fill=tk.BOTH, expand=True)

        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, bg="white", fg="#1f2937")
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)

        # 底部状态栏
        status_frame = tk.Frame(self.root, bg="#e5e7eb", height=25)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(0)

        self.status_bar_var = tk.StringVar(value="准备就绪")
        status_bar = tk.Label(status_frame, textvariable=self.status_bar_var, bg="#e5e7eb", fg="#4b5563", anchor=tk.W)
        status_bar.pack(fill=tk.BOTH, expand=True, padx=10)

    def toggle_batch(self):
        """切换批量处理模式"""
        if self.batch_var.get():
            self.pdf_path_var.set("")
            self.word_path_var.set("")
            for widget in [self.folder_path_var, self.folder_path_var.trace_vinfo()[0][0]]:
                widget.configure(state=tk.NORMAL)
            for entry in [self.pdf_path_var, self.word_path_var]:
                entry.trace_vinfo()[0][0].configure(state=tk.DISABLED)
        else:
            self.folder_path_var.set("")
            for widget in [self.folder_path_var, self.folder_path_var.trace_vinfo()[0][0]]:
                widget.configure(state=tk.DISABLED)
            for entry in [self.pdf_path_var, self.word_path_var]:
                entry.trace_vinfo()[0][0].configure(state=tk.NORMAL)

    def browse_pdf(self):
        """浏览并选择PDF文件"""
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")]
        )
        if file_path:
            self.pdf_path_var.set(file_path)
            # 自动生成Word文件路径
            if not self.word_path_var.get() or self.word_path_var.get() == file_path.replace(".pdf", ".docx"):
                self.word_path_var.set(file_path.replace(".pdf", ".docx"))

    def browse_word(self):
        """浏览并选择Word文件保存位置"""
        if self.pdf_path_var.get():
            initial_file = self.pdf_path_var.get().replace(".pdf", ".docx")
            initial_dir = os.path.dirname(initial_file)
            initial_file_name = os.path.basename(initial_file)
        else:
            initial_dir = ""
            initial_file_name = ""

        file_path = filedialog.asksaveasfilename(
            defaultextension=".docx",
            filetypes=[("Word文件", "*.docx"), ("所有文件", "*.*")],
            initialdir=initial_dir,
            initialfile=initial_file_name
        )
        if file_path:
            self.word_path_var.set(file_path)

    def browse_folder(self):
        """浏览并选择文件夹"""
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path_var.set(folder_path)

    def log(self, message):
        """添加日志消息"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def update_status(self, message):
        """更新状态消息"""
        self.status_var.set(message)
        self.status_bar_var.set(message)

    def update_progress(self, value):
        """更新进度条"""
        self.progress_var.set(value)

    def start_conversion(self):
        """开始转换过程"""
        # 清空日志
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)

        # 检查输入
        if self.batch_var.get():
            folder_path = self.folder_path_var.get()
            if not folder_path or not os.path.isdir(folder_path):
                messagebox.showerror("错误", "请选择有效的文件夹路径")
                return

            # 获取所有PDF文件
            pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
            if not pdf_files:
                messagebox.showinfo("信息", "所选文件夹中没有找到PDF文件")
                return

            # 添加所有PDF文件到任务队列
            for pdf_file in pdf_files:
                pdf_path = os.path.join(folder_path, pdf_file)
                word_path = os.path.join(folder_path, os.path.splitext(pdf_file)[0] + ".docx")
                self.task_queue.put((pdf_path, word_path))

            total_tasks = len(pdf_files)
            self.update_status(f"准备批量转换 {total_tasks} 个PDF文件")
            self.log(f"找到 {total_tasks} 个PDF文件，开始批量转换...")

        else:
            pdf_path = self.pdf_path_var.get()
            word_path = self.word_path_var.get()

            if not pdf_path or not os.path.isfile(pdf_path):
                messagebox.showerror("错误", "请选择有效的PDF文件")
                return

            if not word_path:
                messagebox.showerror("错误", "请指定Word文件保存位置")
                return

            self.task_queue.put((pdf_path, word_path))
            self.update_status("准备转换PDF文件")
            self.log(f"开始转换: {pdf_path}")

    def process_tasks(self):
        """处理转换任务的线程"""
        while True:
            try:
                if not self.task_queue.empty():
                    pdf_path, word_path = self.task_queue.get()

                    # 更新状态
                    self.root.after(0, lambda p=pdf_path: self.update_status(f"正在转换: {os.path.basename(p)}"))

                    try:
                        # 执行转换
                        success = self.convert_pdf(pdf_path, word_path)

                        if success:
                            self.root.after(0, lambda p=word_path: self.log(f"✓ 成功转换为: {p}"))
                        else:
                            self.root.after(0, lambda p=pdf_path: self.log(f"✗ 转换失败: {p}"))

                    except Exception as e:
                        self.root.after(0, lambda msg=str(e): self.log(f"错误: {msg}"))

                    # 标记任务完成
                    self.task_queue.task_done()

                    # 更新进度
                    if self.task_queue.empty():
                        self.root.after(0, lambda: self.update_status("转换完成"))
                        self.root.after(0, lambda: self.update_progress(100))
                        self.root.after(0, lambda: self.log("所有任务已完成"))
                else:
                    time.sleep(0.1)  # 减少CPU使用率
            except Exception as e:
                self.root.after(0, lambda msg=str(e): self.log(f"处理任务时发生错误: {msg}"))

    def convert_pdf(self, pdf_path, word_path):
        """执行PDF到Word的转换"""
        try:
            # 检查PDF文件是否有效
            try:
                with open(pdf_path, 'rb') as file:
                    reader = PdfReader(file)
                    total_pages = len(reader.pages)
                    self.log(f"检测到PDF文件共有 {total_pages} 页")

                    # 检查PDF是否加密
                    if reader.is_encrypted:
                        self.log("错误: PDF文件已加密，无法转换")
                        return False
            except Exception as e:
                self.log(f"错误: 无法读取PDF文件 - {str(e)}")
                return False

            # 创建转换器对象
            cv = Converter(pdf_path)

            # 获取总页数（兼容新版本pdf2docx）
            try:
                # 尝试使用新版本方法
                converter_pages = len(cv._pages)
            except AttributeError:
                # 旧版本方法
                converter_pages = len(cv.doc_reader)

            # 如果pdf2docx获取的页数为0，使用PyPDF2的结果
            if converter_pages == 0:
                converter_pages = total_pages

            self.log(f"开始转换全部 {converter_pages} 页")

            # 转换并显示进度
            self.root.after(0, lambda: self.update_progress(0))

            # 执行转换
            cv.convert(word_path)

            cv.close()
            self.log(f"成功转换 {converter_pages} 页")
            self.update_progress(100)
            return True
        except Exception as e:
            self.log(f"转换过程中发生错误: {str(e)}")
            return False

    def on_closing(self):
        """处理窗口关闭事件"""
        if messagebox.askokcancel("退出", "确定要退出应用程序吗?"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFToWordConverterApp(root)
    root.mainloop()    