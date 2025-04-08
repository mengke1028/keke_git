import win32gui
import win32api
import win32con


def click_window(window_title, x, y, button="left"):
    # 查找窗口句柄
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd == 0:
        print("未找到指定窗口！")
        return

    # 获取窗口位置
    win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
    # 计算相对于屏幕的点击位置
    click_x = x
    click_y = y

    # 生成点击位置的 lParam
    lParam = win32api.MAKELONG(click_x, click_y)

    if button == "left":
        # 模拟鼠标左键按下
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        # 模拟鼠标左键弹起
        win32api.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)
    elif button == "right":
        # 模拟鼠标右键按下
        win32api.SendMessage(hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, lParam)
        # 模拟鼠标右键弹起
        win32api.SendMessage(hwnd, win32con.WM_RBUTTONUP, 0, lParam)


if __name__ == "__main__":
    # 替换为你要点击的窗口标题
    window_title = "微信"
    # 替换为你要点击的相对于窗口左上角的坐标
    click_x = 110
    click_y = 200

    # 模拟左键点击
    click_window(window_title, click_x, click_y, button="left")
    # 模拟右键点击
    # click_window(window_title, click_x, click_y, button="right")
