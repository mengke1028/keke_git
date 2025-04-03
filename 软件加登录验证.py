import os
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from 连接Mysql数据库 import MySQLDatabase
import webbrowser


# 预设的账号和密码
class UI:
    def __init__(self):
        # 创建主窗口
        self.root = None
        self.entry = None
        self.frame = None

    # 主程序窗口
    def open_main_app(self):
        self.root = tk.Tk()
        self.root.title("TTK 示例程序")
        self.frame = ttk.Frame(self.root, padding="10")
        self.entry = ttk.Entry(self.frame)
        # 创建一个框架，用于组织控件
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        # 创建一个标签
        label = ttk.Label(self.frame, text="请输入你的名字:")
        label.grid(row=0, column=0, padx=5, pady=5)
        # 创建一个输入框
        self.entry.grid(row=0, column=1, padx=5, pady=5)

        # 定义一个函数，用于处理按钮点击事件
        def show_name():
            name = self.entry.get()
            result_label.config(text=f"你输入的名字是: {name}")

        # 创建一个按钮
        button = ttk.Button(self.frame, text="显示名字", command=show_name)
        button.grid(row=1, column=0, columnspan=2, pady=10)
        # 创建一个用于显示结果的标签
        result_label = ttk.Label(self.frame, text="")
        result_label.grid(row=2, column=0, columnspan=2, pady=5)
        # 运行主循环
        self.root.mainloop()


def open_baidu(event):
    webbrowser.open('https://68n.cn/n7oi0')


class login(MySQLDatabase):
    def __init__(self):
        super().__init__()
        self.username_entry = None
        self.login_window = None
        # 预设账号密码
        self.CREDENTIALS_FILE = 'credentials.txt'
        self.flog = False

    # 验证登录信息
    def verify_login(self):
        username = self.username_entry.get()
        res = self.shiyongkami(username)
        print('res', res)
        if res[0] is True:
            messagebox.showinfo("登录成功", res[1])
            self.login_window.destroy()
            self.save_credentials(username)
            self.flog = True
        else:
            messagebox.showerror("登录失败", res)

    def run(self):
        # 创建登录窗口
        self.login_window = tk.Tk()
        self.login_window.title("购买+Q 193904974")
        self.login_window.minsize(width=290, height=100)

        # 创建一个框架，用于组织登录控件
        login_frame = ttk.Frame(self.login_window, padding="10")
        login_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 创建账号标签和输入框
        # 创建自定义样式
        style = ttk.Style()
        style.configure("BlueUnderline.TLabel", foreground="blue", font=("TkDefaultFont", 10, "underline"))
        username_label = ttk.Label(login_frame, text="卡密:", style="BlueUnderline.TLabel")

        username_label.grid(row=0, column=0, padx=5, pady=5)
        username_label.bind("<Button-1>", open_baidu)

        self.username_entry = ttk.Entry(login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        # # 创建密码标签和输入框
        # password_label = ttk.Label(login_frame, text="密码:")
        # password_label.grid(row=1, column=0, padx=5, pady=5)
        # self.password_entry = ttk.Entry(login_frame, show="*")
        # self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # 创建登录按钮
        login_button = ttk.Button(login_frame, text="登录", command=self.verify_login)
        login_button.grid(row=2, column=0, columnspan=2, pady=10)
        self.load_credentials()

        # 运行登录窗口的主循环
        self.login_window.mainloop()
        return self.flog

    # 加载之前保存的账号密码
    def load_credentials(self):
        if os.path.exists(self.CREDENTIALS_FILE):

            with open(self.CREDENTIALS_FILE, "r") as file:
                try:
                    username = file.read().splitlines()
                    self.username_entry.insert(0, username)
                except (ValueError, IndexError):
                    pass

    # 保存账号密码到文件
    def save_credentials(self, username):
        with open(self.CREDENTIALS_FILE, "w") as file:
            file.write(f"{username}")


if __name__ == '__main__':
    login = login()
    if not login.run():
        exit()

    ui = UI()
    ui.open_main_app()
