import os
import time
import tkinter as tk
from tkinter import ttk
import random
import threading
import ctypes
import win32gui
from lib2.键盘操作 import key_press
from lib2.鼠标操作 import click, move
from lib2.在当前页面找图找字 import find_pic, mk_OCR
import datetime
from pynput.keyboard import Controller


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("主页")
        self.root.geometry("300x200")

        # 创建按钮框架
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)

        # 创建按钮1 - 打开新窗口并关闭当前窗口
        button1 = tk.Button(button_frame, text="打开新窗口", command=self.open_new_window, width=15, height=2)
        button1.pack(side=tk.LEFT, padx=10)

        # 创建按钮2
        button2 = tk.Button(button_frame, text="按钮2", command=self.on_button2_click, width=10, height=2)
        button2.pack(side=tk.LEFT, padx=10)

    def open_new_window(self):
        # 隐藏当前主窗口
        self.root.withdraw()

        # 创建新窗口
        new_window = tk.Toplevel()
        NewWindow(new_window, self.root)

    def on_button2_click(self):
        print("按钮2被点击")


class NewWindow:
    def __init__(self, window, main_root):
        self.window = window
        self.main_root = main_root
        self.window.title("小鱼干扫拍")
        self.window.geometry("320x550")
        self.window.geometry('+1120+0')
        # 自定义样式
        style = ttk.Style()
        style.configure("Start.TButton",
                        foreground="black",
                        padding=8,
                        font=("宋体", 12),
                        borderwidth=2,
                        relief="solid")

        # 物品名称标签和输入框
        item_label = ttk.Label(self.window, text="物品名称:", font=("宋体", 14))
        item_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.default_value1 = tk.StringVar(value='无色')
        self.item_entry = ttk.Entry(self.window, textvariable=self.default_value1, font=("宋体", 13))
        self.item_entry.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        # 目标价格标签和输入框
        target_price_label = ttk.Label(self.window, text="目标价格:", font=("宋体", 14))
        target_price_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.default_value = tk.StringVar(value=44)
        self.target_price_entry = ttk.Entry(self.window, textvariable=self.default_value, font=("宋体", 13))
        self.target_price_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        # 物品名称标签和输入框
        item_label4 = ttk.Label(self.window, text="随机间隔:", font=("宋体", 14))
        item_label4.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

        self.default_value2 = tk.StringVar(value="2-5")
        self.item_entry4 = ttk.Entry(self.window, textvariable=self.default_value2, font=("宋体", 13))
        self.item_entry4.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        # 点选按钮
        self.var1 = tk.IntVar(value=1)
        check_btn1 = tk.Checkbutton(self.window, text="是否有单价", variable=self.var1, font=("宋体", 11))
        check_btn1.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)

        # 点选按钮
        self.var2 = tk.IntVar(value=1)
        check_btn2 = tk.Checkbutton(self.window, text="需要初始化", variable=self.var2, font=("宋体", 11))
        check_btn2.grid(row=3, column=1, padx=10, pady=10, sticky=tk.W)

        # 扫拍按钮
        self.start_pause_btn = ttk.Button(self.window, text="开始/Home", style="Start.TButton", command=self.start_pause)
        self.start_pause_btn.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)

        # 搓药按钮
        cuoyao_pause_btn = ttk.Button(window, text="开始搓药", style="Start.TButton", command=self.cuoyao)
        # cuoyao_pause_btn.grid(row=4, column=1, padx=10, pady=10, sticky=tk.W)

        # 日志输出文本框
        log_label = ttk.Label(self.window, text="日志输出:", font=("宋体", 12))
        log_label.grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)
        self.log_text = tk.Text(self.window)
        print(tk.W + tk.E + tk.N + tk.S)
        self.log_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)
        # 垂直滚动条
        scrollbar = ttk.Scrollbar(self.window, command=self.log_text.yview)
        scrollbar.grid(row=5, column=2, sticky=tk.NS)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        self.log_text.tag_config("group_info", foreground=get_random_color())
        self.log_text.insert("1.0", f"脚本交流群 578015844 - 欢迎加入\n", "group_info")
        # 设置列权重
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # 创建其他功能按钮
    # func_button = tk.Button(self.window, text="功能按钮", command=self.on_func_button_click, width=15, height=2)
    # func_button.pack(pady=10)

    def go_back(self):
        # 关闭当前窗口
        self.window.destroy()
        # 重新显示主窗口
        self.main_root.deiconify()

    def on_func_button_click(self):
        print("功能按钮被点击")

    def start_pause(self):
        """扫拍"""
        print('开始扫拍')
        global running, thread
        running = not running
        if running:
            self.start_pause_btn.config(text="暂停/Home")
            # 开始新线程执行run函数
            thread = threading.Thread(target=self.run)
            thread.daemon = True
            thread.start()
        else:
            self.start_pause_btn.config(text="开始/Home")
            running = False
            ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), ctypes.py_object(SystemExit))
            print('停止')

    def run(self):
        """全部开始"""
        item_name = self.item_entry.get()
        target_price = self.target_price_entry.get()  # 获取目标价格的值
        entry4 = self.item_entry4.get()

        self.sao(item_name, target_price, entry4)

    def sao(self, item_name, target_price, entry4):
        _name = item_name
        INIT_all()
        if self.var2.get() == 1:
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
            if self.var1.get() == 1:
                jiage = self.OCR(_name)  ##
            else:
                jiage = self.OCR2(_name)  ##
            if jiage is None:
                key_press('ESC')
                time.sleep(1)
                key_press('B')
                find_name(_name)
                continue
            elif jiage <= goumai:
                # print("符合要求开始购买")
                self.log_text.insert("1.0", f"符合要求开始购买\n")
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

    def OCR(self, name):
        timout = time.time() + 15
        while True:
            time.sleep(0.5)
            if timout < time.time():
                return None
            try:
                res = mk_OCR(492, 136, 661, 155, [254, 255], 0.99)
                print(res)
                data = "".join(list(filter(str.isdigit, res)))
                if data != "":
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.log_text.insert("1.0", f"{current_time}-{name}: {data}\n")
                return int(data)
            except:
                continue

    def OCR2(self, name):
        timout = time.time() + 5
        while True:
            time.sleep(0.5)
            if timout < time.time():
                return None
            try:
                res = mk_OCR(520, 127, 624, 145, [182, 181, 183, 255, 254], 0.99)
                print(res)
                data = "".join(list(filter(str.isdigit, res)))
                if data != "":
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.log_text.insert("1.0", f"{current_time}-{name}: {data}\n")
                return int(data)
            except:
                continue

    def cuoyao(self):
        """搓药"""
        print('开始搓药')


# 功能代码#######################################
def INIT_all():
    """初始化窗口"""
    DNF_CK = win32gui.FindWindow("地下城与勇士", "地下城与勇士：创新世纪")
    win32gui.SetForegroundWindow(DNF_CK)
    xpos = 0
    ypos = 0
    width = 800
    length = 600
    win32gui.MoveWindow(DNF_CK, xpos, ypos, width, length, True)
    time.sleep(1)


path = os.path.abspath('.')
print(path)  # 获取当前工作目录路径
path2 = os.path.abspath('../../..')


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


def get_time_now(grace_minutes=5):
    """获取当前时间 小时"""
    now = datetime.datetime.now()
    current_minute = now.minute
    current_hour = now.hour

    # 如果当前分钟大于等于60-grace_minutes（例如50分），则需要等待
    if current_minute >= 60 - grace_minutes:
        next_hour = (current_hour + 1) % 24
        # 计算下一个整点的时间
        target_time = now.replace(hour=next_hour, minute=0, second=0, microsecond=0)
        if next_hour < current_hour:
            target_time += datetime.timedelta(days=1)  # 处理跨天情况
            time.sleep(10 * 60)
            return True


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


def get_random_color():
    """生成随机的十六进制颜色代码"""
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f'#{r:02x}{g:02x}{b:02x}'


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
