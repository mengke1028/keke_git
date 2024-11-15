import uiautomator2 as u2
import time
import os


def click_guangg():
    d.swipe(150, 1100, 750, 1100, duration=0.2)
    time.sleep(0.2)
    d.click(350, 1100)
    time.sleep(20)
    d.click(0.422, 0.085)
    time.sleep(2)


# app = d(text='QQ音乐')
# app.wait(2)
# if app.exists:
#     app.click()
#
# wd = d(text='我的')
# if wd.exists:
#     wd.click()
#
# tx = d(text='提现')
# if tx.exists:
#     tx.click()
# 获取屏幕尺寸


def huadong():
    screen_width, screen_height = d.window_size()
    # 计算每次滑动的起始点和结束点
    start_x = screen_width * 0.5
    start_y = screen_height * 0.8
    end_x = start_x
    end_y = screen_height * 0.2

    # 定义每次滑动的持续时间
    duration = 0.5

    # 向下滚动7页
    for _ in range(7):
        d.swipe(start_x, start_y, end_x, end_y, duration=duration)
        # 可以添加一些等待时间，确保页面加载完成
        time.sleep(1)  # 等待1秒，可以根据实际情况调整

    # 向上滚动7页
    for _ in range(10):
        d.swipe(start_x, end_y, end_x, start_y, duration=duration)
        # 可以添加一些等待时间，确保页面加载完成
        time.sleep(0.2)  # 等待1秒，可以根据实际情况调整

    # 向下滚动7页
    for _ in range(7):
        d.swipe(start_x, start_y, end_x, end_y, duration=duration)
        # 可以添加一些等待时间，确保页面加载完成
        time.sleep(1)  # 等待1秒，可以根据实际情况调整


if __name__ == '__main__':
    d = u2.connect("emulator-5554")
    # d.click(350, 1100)
    # huadong()
    x = 0
    while True:
        click_guangg()
        x += 1
        print('自动看广告', x, '次')
# adb -s emulator-5554 shell input tap 150 200
