# from lib2.键盘操作 import key_press, PressKey, direct_dic, ReleaseKey
import ctypes
import tkinter as tk
import threading
from pynput import keyboard
from tkinter import ttk
import random
import win32gui
import time



def INIT_all():
    """初始化窗口"""
    DNF_CK = win32gui.FindWindow("MapleStoryClass", "MapleStory N - Pioneer Test v.1.0.0")
    win32gui.SetForegroundWindow(DNF_CK)
    xpos = 0
    ypos = 0
    width = 1366
    length = 768
    win32gui.MoveWindow(DNF_CK, xpos, ypos, width, length, True)


def kill_guai(huixue, huilan, zouluyanchi, zouluyanchi_1, bushu, Qyanchi1, Qyanchi2, Wyanchi1, Wyanchi2, Eyanchi1,
              Eyanchi2):
    """杀怪"""
    while True:
        for _ in range(int(bushu)):
            random_float = random.uniform(float(zouluyanchi), float(zouluyanchi_1))
            formatted_float_0_to_1 = f"{random_float:.3f}"

            key_press("RIGHT", float(formatted_float_0_to_1))
            key_press("Q", 0.5, 0.01)
            # key_press("W", 0.5, 0.01)
            # key_press("E", 0.5, 0.01)

        for _ in range(int(bushu)):
            random_float = random.uniform(float(zouluyanchi), float(zouluyanchi_1))
            formatted_float_0_to_1 = f"{random_float:.3f}"

            random_float_Q = random.uniform(float(Qyanchi1), float(Qyanchi2))
            formatted_float_0_to_1_Q = f"{random_float_Q:.3f}"

            random_float_W = random.uniform(float(Wyanchi1), float(Wyanchi2))
            formatted_float_0_to_1_W = f"{random_float_W:.3f}"

            random_float_E = random.uniform(float(Eyanchi1), float(Eyanchi2))
            formatted_float_0_to_1_E = f"{random_float_E:.3f}"

            key_press("LEFT", float(formatted_float_0_to_1))
            key_press("Q", float(formatted_float_0_to_1_Q), 0.01)
            key_press("W", float(formatted_float_0_to_1_W), 0.01)
            key_press("E", float(formatted_float_0_to_1_E), 0.01)


def run():
    """全部开始"""
    # INIT_all()
    time.sleep(1)

    huixue = item_entry.get()  # 回血
    huilan = target_price_entry.get()  # 回蓝
    zouluyanchi = item_entry4.get()  # 走路延迟1
    zouluyanchi_1 = item_entry4_1.get()  # 走路延迟2

    bushu = item_entry5.get()  # 走路步数
    Qyanchi1 = item_jineng1.get()  # Q技能随机延迟1
    Qyanchi2 = item_jineng1_1.get()  # Q技能随机延迟2

    Wyanchi1 = item_jineng2.get()  # W技能随机延迟1
    Wyanchi2 = item_jineng2_1.get()  # W技能随机延迟2

    Eyanchi1 = item_jineng3.get()  # E技能随机延迟1
    Eyanchi2 = item_jineng3_1.get()  # E技能随机延迟2

    print(zouluyanchi, zouluyanchi_1, bushu)
    # sao(item_name, target_price, entry4)
    kill_guai(huixue, huilan, zouluyanchi, zouluyanchi_1, bushu, Qyanchi1, Qyanchi2, Wyanchi1, Wyanchi2, Eyanchi1,
              Eyanchi2)


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


def on_press(key):
    try:
        if key == keyboard.Key.home:
            start_pause()
    except AttributeError:
        pass


if __name__ == '__main__':
    # INIT_all()
    running = False
    thread = None
    running2 = True
    thread2 = None

    window = tk.Tk()
    window.title("冒险岛脚本")
    window.geometry("320x550")
    window.geometry('+378+0')

    # 自定义样式
    style = ttk.Style()
    style.configure("Start.TButton",
                    foreground="black",
                    background="red",
                    padding=8,
                    font=("宋体", 8),
                    borderwidth=2,
                    relief="solid")

    # 自动回血
    item_label = ttk.Label(window, text="自动回血", font=("宋体", 10))
    item_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

    huixue = tk.StringVar(value=400)
    item_entry = ttk.Entry(window, textvariable=huixue, font=("宋体", 10), width=10)
    item_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

    # 自动回蓝
    target_price_label = ttk.Label(window, text="自动回蓝", font=("宋体", 10))
    target_price_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

    default_value = tk.StringVar(value=200)
    target_price_entry = ttk.Entry(window, textvariable=default_value, font=("宋体", 10), width=10)
    target_price_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

    # 走路延迟
    item_label4 = ttk.Label(window, text="走路随机延迟范围", font=("宋体", 10))
    item_label4.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

    default_value1 = tk.StringVar(value=1.7)
    item_entry4 = ttk.Entry(window, textvariable=default_value1, font=("宋体", 10), width=10)
    item_entry4.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

    default_value2 = tk.StringVar(value=1.9)
    item_entry4_1 = ttk.Entry(window, textvariable=default_value2, font=("宋体", 10), width=10)
    item_entry4_1.grid(row=2, column=2, padx=10, pady=10, sticky=tk.W)

    # 走路步数
    item_label5 = ttk.Label(window, text="走路步数", font=("宋体", 10))
    item_label5.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)

    default_value3 = tk.StringVar(value=100)
    item_entry5 = ttk.Entry(window, textvariable=default_value3, font=("宋体", 10), width=10)
    item_entry5.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)

    # 技能释放延迟1
    jineng1 = ttk.Label(window, text="Q技能随机延迟范围", font=("宋体", 10))
    jineng1.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)

    Q_value2 = tk.StringVar(value=0.4)
    item_jineng1 = ttk.Entry(window, textvariable=Q_value2, font=("宋体", 10), width=10)
    item_jineng1.grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)

    Q_value2_1 = tk.StringVar(value=0.6)
    item_jineng1_1 = ttk.Entry(window, textvariable=Q_value2_1, font=("宋体", 10), width=10)
    item_jineng1_1.grid(row=4, column=2, padx=10, pady=10, sticky=tk.W)

    # 技能释放延迟2
    jineng2 = ttk.Label(window, text="W技能随机延迟范围", font=("宋体", 10))
    jineng2.grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)

    W_value2 = tk.StringVar(value=0.5)
    item_jineng2 = ttk.Entry(window, textvariable=W_value2, font=("宋体", 10), width=10)
    item_jineng2.grid(row=5, column=1, padx=10, pady=10, sticky=tk.W)

    W_value2_1 = tk.StringVar(value=0.5)
    item_jineng2_1 = ttk.Entry(window, textvariable=W_value2_1, font=("宋体", 10), width=10)
    item_jineng2_1.grid(row=5, column=2, padx=10, pady=10, sticky=tk.W)

    # 技能释放延迟3
    jineng3 = ttk.Label(window, text="E技能随机延迟范围", font=("宋体", 10))
    jineng3.grid(row=6, column=0, padx=10, pady=10, sticky=tk.W)

    E_value2 = tk.StringVar(value=0.5)
    item_jineng3 = ttk.Entry(window, textvariable=E_value2, font=("宋体", 10), width=10)
    item_jineng3.grid(row=6, column=1, padx=10, pady=10, sticky=tk.W)

    E_value2_1 = tk.StringVar(value=0.5)
    item_jineng3_1 = ttk.Entry(window, textvariable=E_value2_1, font=("宋体", 10), width=10)
    item_jineng3_1.grid(row=6, column=2, padx=10, pady=10, sticky=tk.W)

    # # 点选按钮
    # var1 = tk.IntVar(value=1)
    # check_btn1 = tk.Checkbutton(window, text="是否有单价", variable=var1, font=("宋体", 11))
    # check_btn1.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)

    # 开始按钮
    start_pause_btn = ttk.Button(window, text="开始/Home", style="Start.TButton", command=start_pause)
    start_pause_btn.grid(row=7, column=0, padx=10, pady=10, sticky=tk.W)
    # 停止按钮

    # # 日志输出文本框
    # log_label = ttk.Label(window, text="日志输出:", font=("宋体", 12))
    # log_label.grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)
    # log_text = tk.Text(window)
    # print(tk.W + tk.E + tk.N + tk.S)
    # log_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)
    # # 垂直滚动条
    # scrollbar = ttk.Scrollbar(window, command=log_text.yview)
    # scrollbar.grid(row=5, column=2, sticky=tk.NS)
    # log_text.configure(yscrollcommand=scrollbar.set)
    #
    # # 设置列权重
    # window.grid_columnconfigure(0, weight=1)
    # window.grid_columnconfigure(1, weight=1)

    #
    # start_pause_btn = tk.Button(window, text="开始/Home", command=start_pause)
    # start_pause_btn.pack(padx=20, pady=10)

    window.bind_all("<Home>", start_pause)

    # 开始监听键盘事件
    with keyboard.Listener(on_press=on_press) as listener:
        window.mainloop()
