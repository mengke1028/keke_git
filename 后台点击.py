import win32gui
import win32api
import win32con


def click_window(window_title, x, y, button="left"):
    # 查找窗口句柄
    hwnd = 133662
    print(hwnd)
    if hwnd == 0:
        print("未找到指定窗口！")
        return
    try:
        # 激活窗口!!! 重点
        win32gui.SendMessage(hwnd, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        # 模拟鼠标左键按下
        if button == "left":
            win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, win32api.MAKELONG(x, y))
            # 模拟鼠标左键弹起
            win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, win32api.MAKELONG(x, y))
        elif button == "right":
            # 模拟鼠标右键按下
            win32api.SendMessage(hwnd, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON, win32api.MAKELONG(x, y))
            # 模拟鼠标右键弹起
            win32api.SendMessage(hwnd, win32con.WM_RBUTTONUP, 0, win32api.MAKELONG(x, y))


        print("已模拟鼠标点击")
    except Exception as e:
        print(f"模拟鼠标点击时出现错误: {e}")


if __name__ == "__main__":
    # 替换为你要点击的窗口标题
    window_title = "微信"
    # 替换为你要点击的相对于窗口左上角的坐标

    import time
    time.sleep(3)
    # 模拟左键点击
    click_x = 10
    click_y = 10
    for _ in range(100):
        click_x += 10
        click_y += 10
        # click_window(window_title, click_x, click_y, button="left")
        click_window(window_title, click_x, click_y, button="right")

        time.sleep(1)
    # 模拟右键点击
    # click_window(window_title, click_x, click_y, button="right")
