# -*- coding: utf-8 -*-
# Keke.Meng  2025/3/12 14:59
import json
import os
import tkinter as tk
from tkinter import filedialog
from ctypes import *
import time
from tkinter import ttk
import threading
import ctypes
import datetime
from pynput import keyboard
import webbrowser
import subprocess
import win32gui
import win32con
from libsall.点击在游戏生效 import click, click2
from libsall.tools import find_image_in_region, Find_exit, mk_OCR  # 找图
import pyautogui
from huoyandatil import get_xy

qq_list = []
dd_dll = windll.LoadLibrary(r'tools\dd43390.dll')
dd_dll.DD_btn(0)  # DD Initialize123


def _set_pwd(pwd):
    # 输入密码
    for i in pwd:
        dd_dll.DD_str(i, 1)


class DNFshanghao:
    def __init__(self):
        self.CONFIG_FILE = "tools/config2.json"
        self.qq_list = []
        self.data = []

    def save_config(self):
        config = {
            "path": path_entry.get(),
            "combo_box1": combo_box1.get(),
            "input_entry": input_entry.get(),
        }
        try:
            # 确保保存配置文件的目录存在
            directory = os.path.dirname(self.CONFIG_FILE)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f)
        except Exception as e:
            print(f"保存配置文件时出错: {e}")

    def load_config(self):
        """加载配置"""
        try:
            with open(self.CONFIG_FILE, 'r') as f:
                config = json.load(f)
            path_entry.delete(0, tk.END)
            path_entry.insert(0, config.get("path", ""))
            combo_box1.set(config.get("combo_box1", '选择QQ号'))
            input_entry.delete(0, tk.END)
            input_entry.insert(0, config.get("input_entry", ""))
        except FileNotFoundError:
            print("未找到配置文件，使用默认值。")
        except Exception as e:
            print(f"加载配置文件时出错: {e}")

    def login(self):
        """登录"""
        qq = combo_box1.get()
        self.get_pwd()
        if self.qq_list == '':
            return
        print(self.qq_list)
        for q in self.qq_list:
            if qq == q[0]:
                pwd = q[1]
                # 查找 WeGame 窗口
                wegame_path = r"WeGame"
                # 使用 subprocess.Popen 启动 WeGame
                subprocess.Popen(wegame_path)
                time.sleep(5)
                print('移动窗口')

                wegame_window = win32gui.FindWindow(None, "WeGame")
                if wegame_window:
                    # 将窗口移动到左上角
                    win32gui.MoveWindow(wegame_window, 0, 0, 864, 486, True)

                    # 激活 WeGame 窗口
                    win32gui.SetForegroundWindow(wegame_window)
                    time.sleep(1)  # 等待窗口激活
                    click2(460, 270)
                    click2(460, 270)
                    pyautogui.typewrite(qq)  # 输入qq
                    pyautogui.press('tab')  # 切换到密码输入框
                    time.sleep(0.5)
                    _set_pwd(pwd)  # 输入密码
                    dd_dll.DD_key(313, 1)
                    dd_dll.DD_key(313, 2)  # 回车

                    # 过验证码
                    time.sleep(8)
                    for i in range(3):
                        yanzhegnma = find_image_in_region(464, 5, 1013, 527, 'img/验证码.bmp', 0.98)
                        print(yanzhegnma)
                        if yanzhegnma != -1:
                            print('发现验证码')
                            try:
                                huoyamima = input_entry.get()
                                if huoyamima == '':
                                    return
                                zuobiao = get_xy(huoyamima)  # x y 宽 长
                                for xy in zuobiao:
                                    click(xy[0], xy[1])
                                    time.sleep(1)
                                click(543, 161)
                                time.sleep(10)
                            except:
                                break
                        else:
                            print('无验证码')
                            break

                    # 查找 WeGame 窗口
                    wegame_window = win32gui.FindWindow(None, "WeGame")
                    if wegame_window:
                        # 将窗口最大化
                        win32gui.ShowWindow(wegame_window, win32con.SW_MAXIMIZE)
                        time.sleep(2)
                        resp_mxt = find_image_in_region(237, 5, 1299, 361, 'img/dnf图标.bmp', 0.98)
                        print(resp_mxt)
                        if resp_mxt != -1:
                            X = resp_mxt[1]
                            Y = resp_mxt[2] + 20
                            click2(X, Y)
                            time.sleep(2)
                            dnf_tubiao = find_image_in_region(0, 0, 312, 460, 'img/dnf图标2.bmp', 0.98)
                            if dnf_tubiao != -1:
                                click2(dnf_tubiao[1], dnf_tubiao[2])
                                time.sleep(1)
                            click2(1781, 1002)
                            time.sleep(30)
                        else:
                            print("没有dnf图标")
                        return None

                    else:
                        print("未找到 WeGame 窗口。")

    def stop_all(self):
        """退出wegame 和 dnf"""
        os.system('taskkill /F /IM wegame.exe')
        time.sleep(2)
        os.system('taskkill /F /IM DNF.exe')
        time.sleep(3)

    def get_pwd(self):
        """获取密码"""
        try:
            file_path = path_entry.get()
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    for line in lines:
                        # 打印每行内容，去除行尾的换行符
                        self.qq_list.append(line.strip().split(','))
        except Exception as e:
            print(print(f"读取文件时出现错误: {e}"))

def select_file():
    """选择密码本路径"""
    global qq_list
    qq_list = []
    try:
        file_path = filedialog.askopenfilename()
        if file_path:
            path_entry.delete(0, tk.END)
            path_entry.insert(0, file_path)
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    # 打印每行内容，去除行尾的换行符
                    qq_list.append(line.strip().split(','))
            data = []
            for i in qq_list:
                data.append(i[0])
            combo_box1['values'] = data
            # 清空当前选中的值

    except Exception as e:
        print(print(f"读取文件时出现错误: {e}"))


def run_shanghao():
    """开始上号"""
    global qq_list
    DNF.login()
    while True:
        try:
            # 查找地下城与勇士窗口
            CK = win32gui.FindWindow("地下城与勇士", "地下城与勇士：创新世纪")
            if CK == 0:
                time.sleep(5)
                print('dnf还没启动')
                continue
            else:
                start_button.config(text="开始上号")
                start_button.config(bg="#808080")
                start_button.config(state=tk.NORMAL)
                return
        except Exception as e:
            print("游戏未启动或出现其他错误:", e)
            return False


def start_process():
    """开启线程"""
    global task_thread
    # 创建线程
    start_button.config(text="停止/Home")
    start_button.config(bg="#00FF00")
    start_button.config(state=tk.DISABLED)
    DNF.save_config()
    DNF.stop_all()
    task_thread = threading.Thread(target=run_shanghao)
    # 启动线程
    task_thread.start()



def on_press(key):
    try:
        if key == keyboard.Key.home:
            stop()
    except AttributeError:
        pass


def stop():
    """停止"""
    ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(task_thread.ident), ctypes.py_object(SystemExit))
    start_button.config(text="开始上号", bg="#808080")
    start_button.config(state=tk.NORMAL)


def open_url(event):
    url = "http://www.hyocr.com/"
    webbrowser.open(url)


def on_combobox_open():
    """加载密码"""
    try:
        file_path = path_entry.get()
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    # 打印每行内容，去除行尾的换行符
                    qq_list.append(line.strip().split(','))
            data = []
            for i in qq_list:
                data.append(i[0])
            combo_box1['values'] = data
            # 清空当前选中的值

    except Exception as e:
        print(print(f"读取文件时出现错误: {e}"))


if __name__ == '__main__':
    DNF = DNFshanghao()
    # 创建主窗口
    root = tk.Tk()
    root.title("小鱼干-DNF自动上号脚本QQ:193907974")
    # root.geometry("788x570+1132+0")
    # close_button = tk.Button(root, text="关闭", command=close_window)
    root.attributes('-toolwindow', True)

    # 设置窗口的宽度和高度
    window_width = 440
    window_height = 100

    # 获取屏幕的宽度和高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 计算窗口的 x 和 y 坐标
    x = screen_width - window_width - 10
    y = 0

    # 设置窗口的几何大小和位置
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # 第一排############################################################
    # 创建输入框用于显示文件路径，设置宽度为 300 像素
    path_entry = tk.Entry(root)
    path_entry.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
    # root.columnconfigure(0, minsize=300)

    # 创建选择文件按钮
    select_button = tk.Button(root, text="选择密码本", command=select_file)
    select_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")

    # 创建开始按钮，设置大小为 60x60 像素
    start_button = tk.Button(root, text="开始上号", command=start_process, bg="#808080", relief=tk.RAISED, borderwidth=3,
                             font=("宋体", 14))
    start_button.grid(row=0, column=4, rowspan=5, columnspan=2, padx=5, pady=5, sticky="nsew")
    root.columnconfigure(4, minsize=60)
    root.columnconfigure(5, minsize=60)
    root.rowconfigure(0, minsize=30)
    root.rowconfigure(1, minsize=30)

    # 第二排############################################################
    # 第二排新增 2 个下拉框、一个标签和一个输入框
    combo_box1 = ttk.Combobox(root, state='readonly', width=13)
    combo_box1.set('选择QQ号')  # 设置默认显示内容
    combo_box1.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    combo_box1.bind("<<ComboboxOpen>>", on_combobox_open)

    # 标签
    mingwang = tk.Label(root, text="火眼答题密码:", fg="blue", cursor="hand2")
    mingwang.grid(row=1, column=1, padx=5, pady=5, sticky="e")
    mingwang.bind("<Button-1>", open_url)

    # 输入框
    input_entry = tk.Entry(root, width=13)
    input_entry.grid(row=1, column=2, padx=5, pady=5)
    input_entry.insert(0, "")  # 在输入框索引 0 的位置插入 "0"
    DNF.load_config()
    # 开始监听键盘事件
    with keyboard.Listener(on_press=on_press) as listener:
        on_combobox_open()
        root.mainloop()
