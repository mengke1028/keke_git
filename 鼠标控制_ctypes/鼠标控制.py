import ctypes
import ctypes.wintypes as wintypes
import time

# -------------------------- 终极修复：用 ctypes 原生类型定义 ULONG_PTR --------------------------
# 无需依赖 wintypes.UINT64/UINT32，直接用 ctypes 原生类型
if ctypes.sizeof(ctypes.c_void_p) == 8:  # 64位系统
    ULONG_PTR = ctypes.c_uint64
else:  # 32位系统
    ULONG_PTR = ctypes.c_uint32

# -------------------------- 映射 Windows 底层类型和函数 --------------------------
user32 = ctypes.WinDLL('user32', use_last_error=True)

# 定义 SendInput 所需的结构体（完全兼容所有 Python 版本）
class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        class MOUSEINPUT(ctypes.Structure):
            _fields_ = [
                ("dx", wintypes.LONG),      # 鼠标x坐标（绝对/相对）
                ("dy", wintypes.LONG),      # 鼠标y坐标
                ("mouseData", wintypes.DWORD),  # 滚轮/中键数据
                ("dwFlags", wintypes.DWORD),    # 鼠标事件标志
                ("time", wintypes.DWORD),       # 时间戳
                ("dwExtraInfo", ULONG_PTR)      # 用修复后的 ULONG_PTR
            ]
        _fields_ = [("mi", MOUSEINPUT)]
    _anonymous_ = ("_input",)
    _fields_ = [
        ("type", wintypes.DWORD),  # 输入类型：0=鼠标，1=键盘，2=硬件
        ("_input", _INPUT)
    ]

# 鼠标事件标志
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_ABSOLUTE = 0x8000

# 声明 SendInput 函数原型
user32.SendInput.argtypes = [
    wintypes.UINT,
    ctypes.POINTER(INPUT),
    ctypes.c_int
]
user32.SendInput.restype = wintypes.UINT

# -------------------------- 封装鼠标操作函数 --------------------------
def screen_to_absolute(x, y):
    """将屏幕像素坐标转换为 SendInput 所需的绝对坐标（0-65535 范围）"""
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    abs_x = int(x * 65535 / (screen_width - 1)) if screen_width > 1 else 0
    abs_y = int(y * 65535 / (screen_height - 1)) if screen_height > 1 else 0
    return abs_x, abs_y

def mouse_move_absolute(x, y):
    """移动鼠标到绝对坐标 (x,y)"""
    abs_x, abs_y = screen_to_absolute(x, y)
    input_event = INPUT(
        type=0,
        mi=INPUT._INPUT.MOUSEINPUT(
            dx=abs_x,
            dy=abs_y,
            mouseData=0,
            dwFlags=MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE,
            time=0,
            dwExtraInfo=0
        )
    )
    user32.SendInput(1, ctypes.byref(input_event), ctypes.sizeof(INPUT))

def mouse_click(x, y, button="left"):
    """模拟鼠标点击"""
    mouse_move_absolute(x, y)
    time.sleep(0.05)

    if button == "left":
        down_flag = MOUSEEVENTF_LEFTDOWN
        up_flag = MOUSEEVENTF_LEFTUP
    elif button == "right":
        down_flag = MOUSEEVENTF_RIGHTDOWN
        up_flag = MOUSEEVENTF_RIGHTUP
    else:
        raise ValueError("仅支持 left/right")

    # 构造按下事件
    down_event = INPUT(
        type=0,
        mi=INPUT._INPUT.MOUSEINPUT(
            dx=0, dy=0, mouseData=0, dwFlags=down_flag, time=0, dwExtraInfo=0
        )
    )
    # 构造释放事件
    up_event = INPUT(
        type=0,
        mi=INPUT._INPUT.MOUSEINPUT(
            dx=0, dy=0, mouseData=0, dwFlags=up_flag, time=0, dwExtraInfo=0
        )
    )

    user32.SendInput(1, ctypes.byref(down_event), ctypes.sizeof(INPUT))
    time.sleep(0.05)
    user32.SendInput(1, ctypes.byref(up_event), ctypes.sizeof(INPUT))

# -------------------------- 调用示例 --------------------------
if __name__ == "__main__":
    # 1. 移动鼠标到 (300, 200)
    mouse_move_absolute(300, 200)
    time.sleep(1)

    # 2. 左键单击 (400, 300)
    mouse_click(400, 300, button="left")
    time.sleep(1)

    # 3. 右键单击 (500, 400)
    mouse_click(500, 400, button="right")