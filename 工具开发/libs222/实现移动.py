import win32con
import win32api
import ctypes
import time

key_map = {
    "0": 48, "1": 49, "2": 98, "3": 99, "4": 100, "5": 101, "6": 102, "7": 103, "8": 104, "9": 105,
    "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70, "G": 71, "H": 72, "I": 73, "J": 74,
    "K": 75, "L": 76, "M": 77, "N": 78, "O": 79, "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84,
    "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89, "Z": 90, "LEFT": 37, "UP": 38, "RIGHT": 39, 'ENTER': 13,
    "DOWN": 40, "CTRL": 17, "ALT": 18, "F2": 113, "ESC": 27, "SPACE": 32, "NUM0": 96, "NUM1": 97, "TAB": 9,
    "CAPELOCK": 20, ";": 186, "F12": 123, "PGETDOWN": 34, "PGETUP": 33,
}
direct_dic = {"UP": 0xC8, "DOWN": 0xD0, "LEFT": 0xCB, "RIGHT": 0xCD}


def key_down(key):
    """
    函数功能：按下按键
    参    数：key:按键值
    """
    print("按下", key)
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


def key_press(key, timout=0.02, timout2=0.02):
    """
    函数功能：点击按键（按下并抬起）
    参    数：key:按键值
    """
    key_down(key)
    time.sleep(timout)
    key_up(key)
    time.sleep(timout2)


####################################


SendInput = ctypes.windll.user32.SendInput

W = 0x11
A = 0x1E
S = 0x1F
D = 0x20

M = 0x32
J = 0x24
K = 0x25
LSHIFT = 0x2A
R = 0x13  # 用R代替识破
V = 0x2F

Q = 0x10
I = 0x17
O = 0x18
P = 0x19
C = 0x2E
F = 0x21

up = 0xC8
down = 0xD0
left = 0xCB
right = 0xCD

esc = 0x01

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


"""#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#**#*移动角色#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*"""


def move_right(key='RIGHT'):
    """右奔跑移动"""
    key_press(key)
    key_down(key)


def move_left(key='LEFT'):
    """左奔跑移动"""
    key_press(key)
    key_down(key)


def move_up(key='UP'):
    """上移动"""
    key_down(key)


def move_down(key='DOWN'):
    """下移动"""
    key_down(key)


"""#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*释放技能#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*"""


def get_buff():
    """上buff → → 空格"""
    key_press("RIGHT")
    time.sleep(0.1)
    key_press("RIGHT")
    time.sleep(0.1)
    key_press("SPACE")


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


if __name__ == "__main__":
    time1 = time.time()
    k = "RIGHT"
    while True:
        if abs(time.time() - time1) > 10:
            break
        else:
            # if k not in ["LEFT", "RIGHT", "UP", "DOWN"]:
            #     key_press(k)
            # else:
            #     PressKey(direct_dic[k])
            #     time.sleep(0.1)
            #     ReleaseKey(direct_dic[k])
            #     time.sleep(0.2)
            PressKey(direct_dic[k])
            time.sleep(0.1)
            ReleaseKey(direct_dic[k])
            time.sleep(0.1)
