# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import PyPDF2
from pdf2docx import Converter
import threading


class PDFUtilityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("马伶俐专属工具")
        self.root.geometry("700x550")
        self.root.resizable(True, True)

        # 窗口居中显示
        self.center_window()

        # 设置中文字体支持
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("SimHei", 10))
        self.style.configure("TButton", font=("SimHei", 10))
        self.style.configure("TNotebook.Tab", font=("SimHei", 10))

        # 创建标签页
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建三个功能标签页
        self.tab_convert = ttk.Frame(self.notebook)
        self.tab_split = ttk.Frame(self.notebook)
        self.tab_merge = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_convert, text="PDF转Word")
        self.notebook.add(self.tab_split, text="PDF拆分")
        self.notebook.add(self.tab_merge, text="PDF合并")

        # 初始化各个标签页的UI
        self.init_convert_tab()
        self.init_split_tab()
        self.init_merge_tab()

        # 进度条
        self.progress_frame = ttk.Frame(root)
        self.progress_frame.pack(fill=tk.X, padx=10, pady=5)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)

        self.status_label = ttk.Label(self.progress_frame, text="就绪")
        self.status_label.pack(anchor=tk.W, padx=5, pady=2)

    def center_window(self):
        """将窗口居中显示在屏幕上"""
        # 确保窗口尺寸已更新
        self.root.update_idletasks()

        # 获取屏幕宽度和高度
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # 获取窗口宽度和高度
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        # 计算居中位置
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # 设置窗口位置
        self.root.geometry(f"+{x}+{y}")

    def init_convert_tab(self):
        """初始化PDF转Word标签页"""
        # 源文件选择
        file_frame = ttk.Frame(self.tab_convert)
        file_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(file_frame, text="PDF文件:").pack(side=tk.LEFT, padx=5)

        self.convert_file_path = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.convert_file_path, width=50).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            file_frame,
            text="浏览...",
            command=self.select_convert_file
        ).pack(side=tk.LEFT, padx=5)

        # PDF密码输入
        password_frame = ttk.Frame(self.tab_convert)
        password_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(password_frame, text="PDF密码(如加密):").pack(side=tk.LEFT, padx=5)

        self.pdf_password = tk.StringVar()
        ttk.Entry(password_frame, textvariable=self.pdf_password, show="*", width=30).pack(side=tk.LEFT, padx=5)
        ttk.Label(password_frame, text="(如无密码则留空)").pack(side=tk.LEFT, padx=5)

        # 输出路径选择
        output_frame = ttk.Frame(self.tab_convert)
        output_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(output_frame, text="输出目录:").pack(side=tk.LEFT, padx=5)

        self.convert_output_path = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.convert_output_path, width=50).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            output_frame,
            text="浏览...",
            command=self.select_convert_output
        ).pack(side=tk.LEFT, padx=5)

        # 转换按钮
        btn_frame = ttk.Frame(self.tab_convert)
        btn_frame.pack(fill=tk.X, padx=10, pady=20)

        ttk.Button(
            btn_frame,
            text="开始转换",
            command=self.start_conversion
        ).pack(side=tk.LEFT, padx=50)

    def init_split_tab(self):
        """初始化PDF拆分标签页"""
        # 源文件选择
        file_frame = ttk.Frame(self.tab_split)
        file_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(file_frame, text="PDF文件:").pack(side=tk.LEFT, padx=5)

        self.split_file_path = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.split_file_path, width=50).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            file_frame,
            text="浏览...",
            command=self.select_split_file
        ).pack(side=tk.LEFT, padx=5)

        # PDF密码输入
        password_frame = ttk.Frame(self.tab_split)
        password_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(password_frame, text="PDF密码(如加密):").pack(side=tk.LEFT, padx=5)

        self.split_password = tk.StringVar()
        ttk.Entry(password_frame, textvariable=self.split_password, show="*", width=30).pack(side=tk.LEFT, padx=5)
        ttk.Label(password_frame, text="(如无密码则留空)").pack(side=tk.LEFT, padx=5)

        # 拆分设置
        range_frame = ttk.Frame(self.tab_split)
        range_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(range_frame, text="拆分范围:").pack(side=tk.LEFT, padx=5)

        ttk.Label(range_frame, text="从:").pack(side=tk.LEFT, padx=5)
        self.split_start = tk.StringVar(value="1")
        ttk.Entry(range_frame, textvariable=self.split_start, width=5).pack(side=tk.LEFT)

        ttk.Label(range_frame, text="到:").pack(side=tk.LEFT, padx=5)
        self.split_end = tk.StringVar(value="1")
        ttk.Entry(range_frame, textvariable=self.split_end, width=5).pack(side=tk.LEFT)

        ttk.Label(range_frame, text="(页码从1开始)").pack(side=tk.LEFT, padx=5)

        # 拆分方式选择
        split_type_frame = ttk.Frame(self.tab_split)
        split_type_frame.pack(fill=tk.X, padx=10, pady=10)

        self.split_type = tk.StringVar(value="each_page")
        ttk.Radiobutton(split_type_frame, text="按每页拆分(每页一个文件)",
                        variable=self.split_type, value="each_page").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(split_type_frame, text="按范围拆分(一个文件)",
                        variable=self.split_type, value="range").pack(side=tk.LEFT, padx=10)

        # 输出路径选择
        output_frame = ttk.Frame(self.tab_split)
        output_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(output_frame, text="输出目录:").pack(side=tk.LEFT, padx=5)

        self.split_output_path = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.split_output_path, width=50).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            output_frame,
            text="浏览...",
            command=self.select_split_output
        ).pack(side=tk.LEFT, padx=5)

        # 拆分按钮
        btn_frame = ttk.Frame(self.tab_split)
        btn_frame.pack(fill=tk.X, padx=10, pady=20)

        ttk.Button(
            btn_frame,
            text="开始拆分",
            command=self.start_split
        ).pack(side=tk.LEFT, padx=50)

        # 页码信息
        self.page_count_label = ttk.Label(self.tab_split, text="")
        self.page_count_label.pack(anchor=tk.W, padx=15, pady=5)

    def init_merge_tab(self):
        """初始化PDF合并标签页"""
        # 添加文件区域
        add_frame = ttk.Frame(self.tab_merge)
        add_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(
            add_frame,
            text="添加PDF文件...",
            command=self.add_merge_files
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            add_frame,
            text="移除选中",
            command=self.remove_selected
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            add_frame,
            text="清空列表",
            command=self.clear_merge_list
        ).pack(side=tk.LEFT, padx=5)

        # 密码设置区域
        password_frame = ttk.Frame(self.tab_merge)
        password_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(password_frame, text="文件密码(如加密):").pack(side=tk.LEFT, padx=5)

        self.merge_passwords = {}  # 存储每个文件的密码
        self.current_file_password = tk.StringVar()
        ttk.Entry(password_frame, textvariable=self.current_file_password, show="*", width=30).pack(side=tk.LEFT,
                                                                                                    padx=5)
        ttk.Button(
            password_frame,
            text="应用到选中文件",
            command=self.apply_password_to_selected
        ).pack(side=tk.LEFT, padx=5)

        # 文件列表
        list_frame = ttk.Frame(self.tab_merge)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        ttk.Label(list_frame, text="合并顺序:").pack(anchor=tk.W)

        self.merge_listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE, width=70, height=10)
        self.merge_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.merge_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.merge_listbox.config(yscrollcommand=scrollbar.set)

        # 上下移动按钮
        move_frame = ttk.Frame(list_frame)
        move_frame.pack(side=tk.RIGHT, padx=5)

        ttk.Button(
            move_frame,
            text="上移",
            command=lambda: self.move_item(-1)
        ).pack(fill=tk.X, pady=2)

        ttk.Button(
            move_frame,
            text="下移",
            command=lambda: self.move_item(1)
        ).pack(fill=tk.X, pady=2)

        # 输出路径选择
        output_frame = ttk.Frame(self.tab_merge)
        output_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(output_frame, text="输出文件:").pack(side=tk.LEFT, padx=5)

        self.merge_output_path = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.merge_output_path, width=50).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            output_frame,
            text="浏览...",
            command=self.select_merge_output
        ).pack(side=tk.LEFT, padx=5)

        # 合并按钮
        btn_frame = ttk.Frame(self.tab_merge)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(
            btn_frame,
            text="开始合并",
            command=self.start_merge
        ).pack(side=tk.LEFT, padx=50)

    # 选择文件和路径的函数
    def select_convert_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF文件", "*.pdf")]
        )
        if file_path:
            self.convert_file_path.set(file_path)
            # 默认输出路径设置为源文件所在目录
            self.convert_output_path.set(os.path.dirname(file_path))
            # 清空密码输入
            self.pdf_password.set("")

    def select_convert_output(self):
        output_dir = filedialog.askdirectory()
        if output_dir:
            self.convert_output_path.set(output_dir)

    def select_split_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF文件", "*.pdf")]
        )
        if file_path:
            self.split_file_path.set(file_path)
            # 默认输出路径设置为源文件所在目录
            self.split_output_path.set(os.path.dirname(file_path))
            # 清空密码输入
            self.split_password.set("")
            # 获取页码数
            self.update_page_count(file_path, self.split_password.get())

    def select_split_output(self):
        output_dir = filedialog.askdirectory()
        if output_dir:
            self.split_output_path.set(output_dir)

    def add_merge_files(self):
        file_paths = filedialog.askopenfilenames(
            filetypes=[("PDF文件", "*.pdf")]
        )
        for file_path in file_paths:
            if file_path not in self.merge_listbox.get(0, tk.END):
                self.merge_listbox.insert(tk.END, file_path)
                # 初始化密码为空
                self.merge_passwords[file_path] = ""

    def remove_selected(self):
        selected = self.merge_listbox.curselection()
        if selected:
            file_path = self.merge_listbox.get(selected[0])
            self.merge_listbox.delete(selected)
            # 移除密码记录
            if file_path in self.merge_passwords:
                del self.merge_passwords[file_path]

    def clear_merge_list(self):
        self.merge_listbox.delete(0, tk.END)
        self.merge_passwords.clear()

    def move_item(self, direction):
        selected = self.merge_listbox.curselection()
        if not selected:
            return

        index = selected[0]
        new_index = index + direction

        if 0 <= new_index < self.merge_listbox.size():
            item = self.merge_listbox.get(index)
            self.merge_listbox.delete(index)
            self.merge_listbox.insert(new_index, item)
            self.merge_listbox.selection_set(new_index)

    def apply_password_to_selected(self):
        selected = self.merge_listbox.curselection()
        if not selected:
            messagebox.showwarning("提示", "请先选择一个文件")
            return

        file_path = self.merge_listbox.get(selected[0])
        password = self.current_file_password.get()
        self.merge_passwords[file_path] = password
        messagebox.showinfo("提示", f"密码已应用到文件: {os.path.basename(file_path)}")

    def select_merge_output(self):
        default_filename = "merged.pdf"
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF文件", "*.pdf")],
            initialfile=default_filename
        )
        if file_path:
            self.merge_output_path.set(file_path)

    # 更新PDF页码计数（支持加密文件）
    def update_page_count(self, file_path, password=None):
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                # 检查是否加密
                if reader.is_encrypted:
                    if password:
                        # 尝试解密
                        if not reader.decrypt(password):
                            messagebox.showerror("错误", "密码错误，无法读取PDF内容")
                            return
                    else:
                        messagebox.showwarning("提示", "该PDF文件已加密，请输入密码")
                        return

                page_count = len(reader.pages)
                self.page_count_label.config(text=f"PDF总页数: {page_count}")
                self.split_end.set(str(page_count))
        except Exception as e:
            messagebox.showerror("错误", f"无法读取PDF文件: {str(e)}")

    # 执行转换、拆分、合并的函数（在后台线程中运行）
    def start_conversion(self):
        pdf_path = self.convert_file_path.get()
        output_dir = self.convert_output_path.get()
        password = self.pdf_password.get()

        if not pdf_path or not os.path.exists(pdf_path):
            messagebox.showerror("错误", "请选择有效的PDF文件")
            return

        if not output_dir or not os.path.exists(output_dir):
            messagebox.showerror("错误", "请选择有效的输出目录")
            return

        # 禁用所有按钮防止重复操作
        self.disable_buttons()
        self.status_label.config(text="正在准备转换...")
        self.progress_var.set(0)

        # 在后台线程中执行转换
        threading.Thread(
            target=self.perform_conversion,
            args=(pdf_path, output_dir, password),
            daemon=True
        ).start()

    def perform_conversion(self, pdf_path, output_dir, password):
        try:
            # 获取文件名（不含扩展名）
            file_name = os.path.splitext(os.path.basename(pdf_path))[0]
            docx_path = os.path.join(output_dir, f"{file_name}.docx")

            # 检查PDF是否加密并尝试解密
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                if reader.is_encrypted:
                    if not password:
                        raise Exception("PDF已加密，请提供密码")
                    if not reader.decrypt(password):
                        raise Exception("密码错误，无法解密PDF")

                total_pages = len(reader.pages)

            # 转换PDF到Word
            cv = Converter(pdf_path)

            # 按页转换以更新进度条
            for i in range(total_pages):
                # 传递密码进行转换（如果有）
                kwargs = {"start": i, "end": i + 1}
                if password:
                    kwargs["password"] = password

                cv.convert(docx_path, **kwargs)
                progress = (i + 1) / total_pages * 100
                self.progress_var.set(progress)
                self.status_label.config(text=f"正在转换第 {i + 1}/{total_pages} 页")

            cv.close()

            self.root.after(0, lambda: self.status_label.config(text="转换完成!"))
            self.root.after(0, lambda: self.progress_var.set(100))
            self.root.after(0, lambda: messagebox.showinfo("成功", f"转换完成!\n文件保存至: {docx_path}"))
        except Exception as e:
            print(e)
            self.root.after(0, lambda: messagebox.showerror("转换失败", f"转换过程中出错: {str(e)}"))
            self.root.after(0, lambda: self.status_label.config(text="转换失败"))
        finally:
            self.root.after(0, self.enable_buttons)

    def start_split(self):
        pdf_path = self.split_file_path.get()
        output_dir = self.split_output_path.get()
        password = self.split_password.get()

        if not pdf_path or not os.path.exists(pdf_path):
            messagebox.showerror("错误", "请选择有效的PDF文件")
            return

        if not output_dir or not os.path.exists(output_dir):
            messagebox.showerror("错误", "请选择有效的输出目录")
            return

        try:
            start_page = int(self.split_start.get())
            end_page = int(self.split_end.get())

            if start_page < 1 or end_page < start_page:
                raise ValueError("页码范围无效")
        except ValueError as e:
            messagebox.showerror("错误", f"页码设置错误: {str(e)}")
            return

        # 禁用所有按钮防止重复操作
        self.disable_buttons()
        self.status_label.config(text="正在准备拆分...")
        self.progress_var.set(0)

        # 在后台线程中执行拆分
        threading.Thread(
            target=self.perform_split,
            args=(pdf_path, output_dir, start_page, end_page, password),
            daemon=True
        ).start()

    def perform_split(self, pdf_path, output_dir, start_page, end_page, password):
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)

                # 检查加密状态并解密
                if reader.is_encrypted:
                    if not password:
                        raise Exception("PDF已加密，请提供密码")
                    if not reader.decrypt(password):
                        raise Exception("密码错误，无法解密PDF")

                total_pages = len(reader.pages)

                if end_page > total_pages:
                    end_page = total_pages
                    self.root.after(0, lambda: self.split_end.set(str(total_pages)))

                # 获取文件名（不含扩展名）
                file_name = os.path.splitext(os.path.basename(pdf_path))[0]
                total_pages_to_process = end_page - start_page + 1
                split_type = self.split_type.get()

                if split_type == "each_page":
                    # 按每页拆分，每页生成一个文件
                    for i in range(start_page - 1, end_page):
                        writer = PyPDF2.PdfWriter()
                        writer.add_page(reader.pages[i])

                        # 生成文件名，包含原始文件名和页码
                        page_number = i + 1
                        output_path = os.path.join(output_dir, f"{file_name}_page_{page_number}.pdf")

                        with open(output_path, 'wb') as output_file:
                            writer.write(output_file)

                        # 更新进度
                        progress = (i - start_page + 2) / total_pages_to_process * 100
                        self.root.after(0, lambda p=progress: self.progress_var.set(p))
                        self.root.after(0, lambda p=page_number, t=end_page:
                        self.status_label.config(text=f"正在拆分第 {p}/{t} 页"))

                    self.root.after(0, lambda: messagebox.showinfo(
                        "成功",
                        f"拆分完成!\n共生成 {total_pages_to_process} 个文件\n保存至: {output_dir}"
                    ))
                else:
                    # 按范围拆分，生成一个文件
                    writer = PyPDF2.PdfWriter()

                    # 添加指定范围的页面
                    for i in range(start_page - 1, end_page):
                        writer.add_page(reader.pages[i])
                        progress = (i - start_page + 2) / total_pages_to_process * 100
                        self.root.after(0, lambda p=progress: self.progress_var.set(p))

                    # 保存拆分后的PDF
                    output_path = os.path.join(output_dir, f"{file_name}_pages_{start_page}-{end_page}.pdf")

                    with open(output_path, 'wb') as output_file:
                        writer.write(output_file)

                    self.root.after(0, lambda: messagebox.showinfo(
                        "成功",
                        f"拆分完成!\n文件保存至: {output_path}"
                    ))

                self.root.after(0, lambda: self.status_label.config(text="拆分完成!"))
                self.root.after(0, lambda: self.progress_var.set(100))

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("拆分失败", f"拆分过程中出错: {str(e)}"))
            self.root.after(0, lambda: self.status_label.config(text="拆分失败"))
        finally:
            self.root.after(0, self.enable_buttons)

    def start_merge(self):
        files = self.merge_listbox.get(0, tk.END)
        output_path = self.merge_output_path.get()

        if not files:
            messagebox.showerror("错误", "请添加至少一个PDF文件")
            return

        if not output_path:
            messagebox.showerror("错误", "请选择输出文件路径")
            return

        # 检查所有文件是否存在
        for file in files:
            if not os.path.exists(file):
                messagebox.showerror("错误", f"文件不存在: {file}")
                return

        # 禁用所有按钮防止重复操作
        self.disable_buttons()
        self.status_label.config(text="正在准备合并...")
        self.progress_var.set(0)

        # 在后台线程中执行合并
        threading.Thread(
            target=self.perform_merge,
            args=(files, output_path, self.merge_passwords),
            daemon=True
        ).start()

    def perform_merge(self, files, output_path, passwords):
        try:
            writer = PyPDF2.PdfWriter()
            total_files = len(files)
            total_pages = 0

            for i, file_path in enumerate(files):
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)

                    # 检查加密状态并解密
                    if reader.is_encrypted:
                        password = passwords.get(file_path, "")
                        if not password:
                            raise Exception(f"文件 '{os.path.basename(file_path)}' 已加密，请提供密码")
                        if not reader.decrypt(password):
                            raise Exception(f"文件 '{os.path.basename(file_path)}' 密码错误")

                    # 添加所有页面
                    for page in reader.pages:
                        writer.add_page(page)
                        total_pages += 1

                # 更新进度
                progress = (i + 1) / total_files * 100
                self.root.after(0, lambda p=progress: self.progress_var.set(p))
                self.root.after(0, lambda i=i + 1, t=total_files: self.status_label.config(text=f"正在合并第 {i}/{t} 个文件"))

            # 保存合并后的PDF
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)

            self.root.after(0, lambda: self.status_label.config(text="合并完成!"))
            self.root.after(0, lambda: self.progress_var.set(100))
            self.root.after(0, lambda: messagebox.showinfo("成功", f"合并完成!\n共合并 {total_pages} 页\n文件保存至: {output_path}"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("合并失败", f"合并过程中出错: {str(e)}"))
            self.root.after(0, lambda: self.status_label.config(text="合并失败"))
        finally:
            self.root.after(0, self.enable_buttons)

    # 禁用/启用所有按钮
    def disable_buttons(self):
        for frame in [self.tab_convert, self.tab_split, self.tab_merge]:
            for widget in frame.winfo_children():
                if isinstance(widget, ttk.Button) or isinstance(widget, tk.Button):
                    widget.config(state=tk.DISABLED)

    def enable_buttons(self):
        for frame in [self.tab_convert, self.tab_split, self.tab_merge]:
            for widget in frame.winfo_children():
                if isinstance(widget, ttk.Button) or isinstance(widget, tk.Button):
                    widget.config(state=tk.NORMAL)


if __name__ == "__main__":
    # 检查并提示需要安装的库
    required_libraries = {
        "PyPDF2": "pypdf2",
        "pdf2docx": "pdf2docx"
    }

    missing = []
    for lib, pkg in required_libraries.items():
        try:
            __import__(lib)
        except ImportError:
            missing.append(pkg)

    if missing:
        print("检测到缺少必要的库，请先安装：")
        print(f"pip install {' '.join(missing)}")
    else:
        root = tk.Tk()
        app = PDFUtilityApp(root)
        root.mainloop()