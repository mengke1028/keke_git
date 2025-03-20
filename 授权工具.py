import tkinter as tk
from tkinter import ttk
import os
from tkinter import messagebox

class login:
    def __init__(self):
        super().__init__()
        self.username_entry = None
        self.password_entry = None
        self.login_window = None
        # 预设账号密码
        self.CORRECT_USERNAME = "1"
        self.CORRECT_PASSWORD = "2"
        self.CREDENTIALS_FILE = 'credentials.txt'
        self.flog = False

    # 验证登录信息
    def verify_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == self.CORRECT_USERNAME and password == self.CORRECT_PASSWORD:
            self.login_window.destroy()
            self.save_credentials(username, password)
            self.flog = True
        else:
            messagebox.showerror("登录失败", "账号或密码错误，请重试。")

    def run(self):
        # 创建登录窗口
        self.login_window = tk.Tk()
        self.login_window.title("登录")
        # 获取屏幕宽度和高度
        screen_width = self.login_window.winfo_screenwidth()
        screen_height = self.login_window.winfo_screenheight()

        # 计算登录窗口的 x 和 y 坐标，使窗口居中
        x = screen_width // 3
        y = screen_height // 3
        # 设置登录窗口的位置和大小
        self.login_window.geometry(f"+{x}+{y}")
        # self.login_window.geometry(f"{login_window_width}x{login_window_height}+{x}+{y}")


        # 创建一个框架，用于组织登录控件
        login_frame = ttk.Frame(self.login_window, padding="10")
        login_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 创建账号标签和输入框
        username_label = ttk.Label(login_frame, text="账号:")
        username_label.grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        # 创建密码标签和输入框
        password_label = ttk.Label(login_frame, text="密码:")
        password_label.grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

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
                    username, password = file.read().splitlines()
                    self.username_entry.insert(0, username)
                    self.password_entry.insert(0, password)
                except (ValueError, IndexError):
                    pass

    # 保存账号密码到文件
    def save_credentials(self, username, password):
        with open(self.CREDENTIALS_FILE, "w") as file:
            file.write(f"{username}\n{password}")


def submit_new_machine_code():
    machine_code = entry_machine_code.get()
    expiration_time = combo_expiration.get()
    print(f"新机器码: {machine_code}, 到期时间: {expiration_time}")


def submit_replace_machine_code():
    old_machine_code = entry_old_machine_code.get()
    new_machine_code = entry_new_machine_code.get()
    print(f"旧机器码: {old_machine_code}, 新机器码: {new_machine_code}")


def update_machine_code():
    print("点击了更新机器码按钮")

    button_submit_new.config(state=tk.NORMAL)
    button_submit_replace.config(state=tk.NORMAL)


if __name__ == '__main__':
    login = login()
    if not login.run():
        exit()

    root = tk.Tk()
    root.title("机器码管理")
    # 获取屏幕宽度和高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 窗口的宽度和高度
    window_width = 350
    window_height = 450

    # 计算窗口的 x 和 y 坐标，使窗口居中
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # 设置窗口的位置和大小
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.configure(bg="#f0f0f0")

    # 设置字体样式
    font_style = ("Arial", 12)

    # 第一部分：输入新机器码和选择到期时间
    frame_new = tk.Frame(root, padx=20, pady=20, bg="#f0f0f0")
    frame_new.pack(pady=10)

    label_machine_code = tk.Label(frame_new, text="机器码:", font=font_style, bg="#f0f0f0", anchor=tk.E)
    label_machine_code.grid(row=0, column=0, sticky=tk.E, pady=5)

    entry_machine_code = tk.Entry(frame_new, font=font_style)
    entry_machine_code.grid(row=0, column=1, pady=5)

    label_expiration = tk.Label(frame_new, text="授权时长:", font=font_style, bg="#f0f0f0", anchor=tk.E)
    label_expiration.grid(row=1, column=0, sticky=tk.E, pady=5)

    expiration_options = ["一个月", "永久"]
    # 设置 Combobox 的宽度
    combo_expiration = ttk.Combobox(frame_new, values=expiration_options, font=font_style, width=18, state="readonly")
    combo_expiration.grid(row=1, column=1, pady=5, sticky=tk.W)
    combo_expiration.set(expiration_options[0])

    button_submit_new = tk.Button(frame_new, text="对机器码授权", command=submit_new_machine_code,
                                  font=font_style, bg="#4CAF50", fg="white", width=15, state=tk.DISABLED)
    button_submit_new.grid(row=2, column=0, columnspan=2, pady=20)

    # 更新机器码按钮
    button_update = tk.Button(root, text="更新数据", command=update_machine_code,
                              font=font_style, bg="#2196F3", fg="white", width=15)
    button_update.pack(pady=10)

    # 第二部分：替换机器码
    frame_replace = tk.Frame(root, padx=20, pady=20, bg="#f0f0f0")
    frame_replace.pack(pady=10)

    label_old_machine_code = tk.Label(frame_replace, text="旧机器码:", font=font_style, bg="#f0f0f0", anchor=tk.E)
    label_old_machine_code.grid(row=0, column=0, sticky=tk.E, pady=5)

    entry_old_machine_code = tk.Entry(frame_replace, font=font_style)
    entry_old_machine_code.grid(row=0, column=1, pady=5)

    label_new_machine_code = tk.Label(frame_replace, text="新机器码:", font=font_style, bg="#f0f0f0", anchor=tk.E)
    label_new_machine_code.grid(row=1, column=0, sticky=tk.E, pady=5)

    entry_new_machine_code = tk.Entry(frame_replace, font=font_style)
    entry_new_machine_code.grid(row=1, column=1, pady=5)

    button_submit_replace = tk.Button(frame_replace, text="机器码换绑", command=submit_replace_machine_code,
                                      font=font_style, bg="#4CAF50", fg="white", width=15, state=tk.DISABLED)
    button_submit_replace.grid(row=2, column=0, columnspan=2, pady=20)

    root.mainloop()
