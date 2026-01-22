import time

import win32con
import win32api
from pynput.keyboard import Key, Controller


"""
      keybd_event(bVk, bScan, dwFlags, dwExtraInfo)
      第一个参数：虚拟键码（键盘键码对照表见附录）；
      第二个参数：硬件扫描码，一般设置为0即可；
      第三个参数：函数操作的一个标志位，如果值为KEYEVENTF_EXTENDEDKEY则该键被按下，也可设置为0即可，如果值为KEYEVENTF_KEYUP则该按键被释放；
      第四个参数：定义与击键相关的附加的32位值，一般设置为0即可。
      https://blog.csdn.net/lihuarongaini/article/details/101298063
"""


def click(X, Y,tim = 0.1):
    # 移动到指定坐标
    win32api.SetCursorPos([X, Y])
    time.sleep(0.01)
    # 模拟鼠标左键按下。
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.02)
    # 模拟鼠标左键放开。
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(0.02)

def only_move(X,Y):
    win32api.SetCursorPos([X, Y])
    time.sleep(0.01)

# 移动到指定坐标

def click_right(X, Y):
    # 移动到指定坐标
    win32api.SetCursorPos([X, Y])
    # 模拟鼠标左键按下。
    for i in range(1):
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
        time.sleep(0.1)
        # 模拟鼠标左键放开。
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
        time.sleep(0.01)

def click_move(X1, Y1,X2, Y2):
    # 拖动
    win32api.SetCursorPos([X1, Y1])
    # 模拟鼠标左键按下。
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.1)
    win32api.SetCursorPos([X2, Y2])
    # 模拟鼠标左键放开。
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(0.01
)


def sent_name():
    msg = "hello"
    keyboard = Controller()
    keyboard.type("1234556")


key_map = {
    "0": 96, "1": 97, "2": 98, "3": 99, "4": 100, "5": 101, "6": 102, "7": 103, "8": 104, "9": 105,
    "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70, "G": 71, "H": 72, "I": 73, "J": 74,
    "K": 75, "L": 76, "M": 77, "N": 78, "O": 79, "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84,
    "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89, "Z": 90, "LEFT": 37, "UP": 38, "RIGHT": 39, 'ENTER': 13,
    "DOWN": 40, "CTRL": 17, "ALT": 18, "F2": 113, "ESC": 27, "SPACE": 32, "NUM0": 96, "NUM1": 97, "TAB": 9
}
direct_dic = {"UP": 0xC8, "DOWN": 0xD0, "LEFT": 0xCB, "RIGHT": 0xCD}


def key_down(key):
    """
    函数功能：按下按键
    参    数：key:按键值
    """
    key = key.upper()
    vk_code = key_map[key]
    win32api.keybd_event(vk_code, win32api.MapVirtualKey(vk_code, 0), 0, 0)


def key_up(key):
    """
    函数功能：抬起按键
    参    数：key:按键值
    """
    key = key.upper()
    vk_code = key_map[key]
    win32api.keybd_event(vk_code, win32api.MapVirtualKey(vk_code, 0), win32con.KEYEVENTF_KEYUP, 0)


def key_press(key):
    """
    函数功能：点击按键（按下并抬起）
    参    数：key:按键值
    """
    # key_down(key)
    # time.sleep(0.07)
    # key_up(key)
    # time.sleep(0.07)

    win32api.keybd_event(65, 0, 0, 0)  # P
    win32api.keybd_event(65, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放指令


