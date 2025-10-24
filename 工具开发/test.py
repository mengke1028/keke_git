# -*- coding: utf-8 -*-
# Keke.Meng  2025/6/25 15:28
import ctypes
import tkinter as tk
import threading
from pynput import keyboard
from tkinter import ttk

import time, random
from lib2.鼠标操作 import click, move
from lib2.键盘操作 import key_press
from lib2.在当前页面找图找字 import find_pic, mk_OCR
from pynput.keyboard import Controller
import os
import win32gui
import datetime
from datetime import datetime
import wmi


def get_cpu_serial_number():
    try:
        c = wmi.WMI()
        for processor in c.Win32_Processor():
            cpu = processor.ProcessorId.strip()
            return str(cpu)
    except Exception as e:
        print(f"获取 CPU 序列号时出错: {e}")
        return None


# 获取cpu序列号
computer_name = get_cpu_serial_number()
from lib2.jintu import get_IP

path = os.path.abspath('.')
print(path)  # 获取当前工作目录路径
path2 = os.path.abspath('../../..')

operation = None


class Operation:

    def __init__(self):
        self.hwnd = win32gui.FindWindow("地下城与勇士", "地下城与勇士：创新世纪")
        xpos = 0
        ypos = 0
        width = 800
        length = 600
        win32gui.MoveWindow(self.hwnd, xpos, ypos, width, length, True)
        win32gui.SetForegroundWindow(self.hwnd)  # 激活游戏窗口
        time.sleep(1)
        print("游戏窗口置顶")


def OCR(name):
    timout = time.time() + 15
    while True:
        time.sleep(0.5)
        if timout < time.time():
            return None
        try:
            res = mk_OCR(492, 136, 661, 155, [254, 255], 0.99)
            print(res)
            # res = wegame.ALL.dm.Ocr(492, 136, 661, 155, "", "ffb500-000000", 1.0, 0, 0, 0, 0, "", '')
            data = "".join(list(filter(str.isdigit, res)))
            if data != "":
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_text.insert("1.0", f"{current_time}-{name}: {data}\n")
            return int(data)
        except:
            continue


def OCR2(name):
    timout = time.time() + 15
    while True:
        time.sleep(0.5)
        if timout < time.time():
            return None
        try:
            res = mk_OCR(520, 127, 624, 145, [182, 181, 183, 255, 254], 0.99)
            print(res)
            # res = wegame.ALL.dm.Ocr(492, 136, 661, 155, "", "ffb500-000000", 1.0, 0, 0, 0, 0, "", '')
            data = "".join(list(filter(str.isdigit, res)))
            if data != "":
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_text.insert("1.0", f"{current_time}-{name}: {data}\n")
            return int(data)
        except:
            continue


def int_paimai():
    """打开拍卖行 并初始化"""
    global moren
    while True:
        key_press("B")
        time.sleep(0.1)
        resp = find_pic(path + r"\img\默认.bmp")
        if resp:
            print("拍卖行打开")
            moren = resp

            click(resp[0], resp[1])
            return

        key_press("ESC")
        time.sleep(0.5)


def find_name(name):
    """输入要扫的材料名"""
    morenX = moren[0]
    morenY = moren[1]
    click(morenX, morenY)
    time.sleep(0.5)
    click(55, 89)
    keyboard = Controller()
    keyboard.type(name)
    time.sleep(0.5)
    click(658, 89)  # 点击搜索


from datetime import datetime, timedelta

def get_time_now(grace_minutes=5):
    """获取当前时间 小时"""
    now = datetime.now()
    current_minute = now.minute
    current_hour = now.hour

    # 如果当前分钟大于等于60-grace_minutes（例如50分），则需要等待
    if current_minute >= 60 - grace_minutes:
        next_hour = (current_hour + 1) % 24
        # 计算下一个整点的时间
        target_time = now.replace(hour=next_hour, minute=0, second=0, microsecond=0)
        if next_hour < current_hour:
            target_time += timedelta(days=1)  # 处理跨天情况
            time.sleep(10 * 60)
            return True


import random


def generate_random_number(min_val=1.0, max_val=3.0, precision=1):
    """
    生成指定区间内的随机小数，精确到指定小数位数

    参数:
    - min_val: 最小值 (包含)
    - max_val: 最大值 (包含)
    - precision: 小数位数
    """
    # 生成随机浮点数
    random_num = random.uniform(min_val, max_val)

    # 按指定精度舍入
    rounded_num = round(random_num, precision)

    # 确保结果不小于最小值（由于舍入可能导致微小偏差）
    if rounded_num < min_val:
        rounded_num = min_val
    elif rounded_num > max_val:
        rounded_num = max_val

    return rounded_num


def sao(item_name, target_price, entry4):
    Operation()  # 525484
    _name = item_name
    if var2.get() == 1:
        print('需要初始化')
        int_paimai()
        find_name(_name)

    goumai = int(target_price)  # 购买的最高价格
    i = 0
    while True:
        i += 1
        if i > 100:
            i = 0
            time.sleep(20)
        if get_time_now():  # 判断12点
            guanbi = find_pic(path + r"\img\关闭.bmp")
            if guanbi != -1:
                print('找到关闭')
                time.sleep(1)
                click(guanbi[1], guanbi[2])
                time.sleep(1)
        # t = random.uniform(1.5, 4)
        if '-' in entry4:
            datasss = entry4.split('-')
            entry = generate_random_number(int(datasss[0]), int(datasss[-1]))
        else:
            entry = float(entry4)
        time.sleep(entry)
        key_press('ENTER')
        click(658, 89)  # 点击搜索按钮
        move(632, 141)
        if var1.get() == 1:
            jiage = OCR(_name)  ##
        else:
            jiage = OCR2(_name)  ##
        if jiage is None:
            key_press('ESC')
            time.sleep(1)
            key_press('B')
            find_name(_name)
            continue
        elif jiage <= goumai:
            # print("符合要求开始购买")
            log_text.insert("1.0", f"符合要求开始购买\n")
            click(623, 137)  # 点击物品
            time.sleep(0.1)
            click(623, 140)  # 点击购买
            time.sleep(0.1)
            key_press('ENTER')  # 输入回车
            click(623, 140)  # 点击购买
            key_press('ENTER')  # 再输入回车
            key_press('ENTER')  # 再输入回车
            key_press('ENTER')  # 再输入回车
            key_press('ENTER')  # 再输入回车
            time.sleep(0.5)
            key_press('SPACE')


def on_press(key):
    try:
        if key == keyboard.Key.home:
            start_pause()
    except AttributeError:
        pass

    global running2
    try:
        if key == keyboard.Key.esc:
            if running2:
                running2 = True
            else:
                cuoyao()
    except AttributeError:
        pass


def INIT_all():
    """初始化窗口"""
    DNF_CK = win32gui.FindWindow("地下城与勇士", "地下城与勇士：创新世纪")
    win32gui.SetForegroundWindow(DNF_CK)
    xpos = 0
    ypos = 0
    width = 800
    length = 600
    win32gui.MoveWindow(DNF_CK, xpos, ypos, width, length, True)


def run2():
    while True:
        click(484, 442)
        time.sleep(2)


def run():
    """全部开始"""
    INIT_all()
    time.sleep(1)

    item_name = item_entry.get()
    target_price = target_price_entry.get()  # 获取目标价格的值
    entry4 = item_entry4.get()

    sao(item_name, target_price, entry4)


def start_pause():
    global running, thread
    running = not running
    if running:
        start_pause_btn.config(text="暂停/Home")
        # 开始新线程执行run函数
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()
    else:
        start_pause_btn.config(text="开始/Home")
        running = False
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), ctypes.py_object(SystemExit))
        print('停止')


def cuoyao():
    global running2, thread2
    INIT_all()

    if running2:
        cuoyao_pause_btn.config(text="暂停/ESC")
        # 开始新线程执行run函数
        thread2 = threading.Thread(target=run2)
        thread2.daemon = True
        thread2.start()
        log_text.insert("1.0", f"开始搓药\n")
        print('开始了')
        running2 = False
    else:
        cuoyao_pause_btn.config(text="开始搓药")
        log_text.insert("1.0", f"暂停搓药\n")

        running2 = True
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread2.ident), ctypes.py_object(SystemExit))
        print('停止')


if __name__ == '__main__':
    running = False
    thread = None
    running2 = True
    thread2 = None

    window = tk.Tk()
    window.title("小鱼干扫拍")
    window.geometry("320x550")
    window.geometry('+1120+0')

    # 自定义样式
    style = ttk.Style()
    style.configure("Start.TButton",
                    foreground="black",
                    background="red",
                    padding=8,
                    font=("宋体", 12),
                    borderwidth=2,
                    relief="solid")

    # 物品名称标签和输入框
    item_label = ttk.Label(window, text="物品名称:", font=("宋体", 14))
    item_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

    default_value1 = tk.StringVar(value='无色')
    item_entry = ttk.Entry(window, textvariable=default_value1, font=("宋体", 13))
    item_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

    # 目标价格标签和输入框
    target_price_label = ttk.Label(window, text="目标价格:", font=("宋体", 14))
    target_price_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

    default_value = tk.StringVar(value=44)
    target_price_entry = ttk.Entry(window, textvariable=default_value, font=("宋体", 13))
    target_price_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

    # 物品名称标签和输入框
    item_label4 = ttk.Label(window, text="随机间隔:", font=("宋体", 14))
    item_label4.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

    default_value2 = tk.StringVar(value="2-5")
    item_entry4 = ttk.Entry(window, textvariable=default_value2, font=("宋体", 13))
    item_entry4.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

    # 点选按钮
    var1 = tk.IntVar(value=1)
    check_btn1 = tk.Checkbutton(window, text="是否有单价", variable=var1, font=("宋体", 11))
    check_btn1.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)

    # 点选按钮
    var2 = tk.IntVar(value=0)
    check_btn2 = tk.Checkbutton(window, text="需要初始化", variable=var2, font=("宋体", 11))
    check_btn2.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)

    # 开始按钮
    start_pause_btn = ttk.Button(window, text="开始/Home", style="Start.TButton", command=start_pause)
    start_pause_btn.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
    # 停止按钮
    cuoyao_pause_btn = ttk.Button(window, text="开始搓药", style="Start.TButton", command=cuoyao)
    # cuoyao_pause_btn.grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)

    # 日志输出文本框
    log_label = ttk.Label(window, text="日志输出:", font=("宋体", 12))
    log_label.grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)
    log_text = tk.Text(window)
    print(tk.W + tk.E + tk.N + tk.S)
    log_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)
    # 垂直滚动条
    scrollbar = ttk.Scrollbar(window, command=log_text.yview)
    scrollbar.grid(row=5, column=2, sticky=tk.NS)
    log_text.configure(yscrollcommand=scrollbar.set)
    log_text.tag_config("group_info", foreground="#d51f74")
    log_text.insert("1.0", f"脚本交流群 578015844 - 欢迎加入\n", "group_info")
    # 设置列权重
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)

    #
    # start_pause_btn = tk.Button(window, text="开始/Home", command=start_pause)
    # start_pause_btn.pack(padx=20, pady=10)

    window.bind_all("<Home>", start_pause)

    # 开始监听键盘事件
    with keyboard.Listener(on_press=on_press) as listener:
        window.mainloop()
