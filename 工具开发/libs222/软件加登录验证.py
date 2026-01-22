import os
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import webbrowser
import mysql.connector
from mysql.connector import Error
import time

class MySQLDatabase:
    def __init__(self):
        self.host = '172.81.247.38'
        self.database = 'keke_test'
        self.user = 'keke'
        self.password = 'mengke1028..'
        self.connection = None
        self.create_connection()

    def create_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print('Connected to MySQL database')
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")

    def add_code(self, key):
        # 往数据库增加卡密
        insert_query = f"INSERT INTO activation_codes (activation_code, start_time, is_destroyed) VALUES ('{key}', NULL ,0)"
        cursor = self.connection.cursor()
        if insert_query:
            cursor.execute(insert_query)
            self.connection.commit()
            print("Query executed successfully")

    def read_query(self):
        # 查询全部的数据
        query = "SELECT * FROM activation_codes"
        if self.connection:
            cursor = self.connection.cursor()
            result = None
            try:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
            except Error as e:
                print(f"Error while reading query: {e}")

    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print('Connection to MySQL database closed')

    def update_code(self, key):
        """更新卡密状态为 1 并记录当前时间 """
        current_time = str(int(time.time()))
        update_query = "UPDATE activation_codes SET start_time = %s, is_destroyed = 1 WHERE activation_code = %s"
        values = (current_time, key)

        cursor = self.connection.cursor()
        cursor.execute(update_query, values)
        rows_affected = cursor.rowcount
        self.connection.commit()
        if rows_affected == 0:
            print(f"卡密 {key} 可能不存在")
            return False
        else:
            return True

    def query_by_activation_code(self, activation_code):
        """根据 activation_code 查询记录"""
        query = "SELECT * FROM activation_codes WHERE activation_code = %s"
        values = (activation_code,)
        if self.connection:
            cursor = self.connection.cursor()
            try:
                cursor.execute(query, values)
                result = cursor.fetchall()
                return result
            except Error as e:
                print(f"查询数据时出现错误: {e}")
        return None

    def shiyongkami(self, activation_code):
        """使用卡密 """
        data = self.query_by_activation_code(activation_code)

        if not data:
            return '卡密不存在'
        stat_time = data[0][1]
        if stat_time is None:
            # 执行修改
            try:
                self.update_code(activation_code)
                print(f'{activation_code} 状态修改成 1, 记录时间')
                return True, f'卡密还有{4}小时过期'
            except Exception as e:
                print(e)
                print(f"卡密 {activation_code} 可能不存在")
                return '卡密错误'
        else:
            low_time = int(time.time()) - int(stat_time)
            if low_time > 14400:  # 4小时试用期
                return '试用超时了'
            else:
                print(f'卡密还有{int((14400-low_time)/3600)}小时过期')
                return True, f'卡密还有{int((14400-low_time)/3600)}小时过期'


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

