# -*- coding: utf-8 -*-
# Keke.Meng  2025/3/5 11:11
import tkinter as tk
from ctypes import *

# 创建主窗口
root = tk.Tk()
root.title("密码输入测试")

# 创建标签
label = tk.Label(root, text="点击输入密码后，3秒内移动光标到密码框")
label.pack(pady=20)


# 创建按钮
def on_button_click():
    label.config(text="按钮被点击了！")
    import time

    print("Load DD!")

    dd_dll = windll.LoadLibrary('dd43390.dll')
    time.sleep(2)

    st = dd_dll.DD_btn(0)  # DD Initialize
    print(1)
    if st == 1:
        print("OK")
    else:
        print("Error")
        exit(101)
    time.sleep(1)
    for i in ['A', '1', 'a', '.', '@']:
        dd_dll.DD_str(i)


button = tk.Button(root, text="输入密码", command=on_button_click)
button.pack(pady=10)

# 运行主循环
root.mainloop()
