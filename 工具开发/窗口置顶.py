import tkinter as tk
from PIL import Image
import io
import pystray


def quit_window(icon):
    icon.stop()
    root.destroy()


def show_window(icon, item):
    icon.stop()
    root.after(0, root.deiconify)


def on_clicked(icon, item):
    if item == 1:
        print("1")
    elif item == 2:
        print(2)
    else:
        print(3)


def withdraw_window():
    try:
        root.withdraw()
        image = Image.open("icon.png")  # 指定你的PNG图标文件路径
        buffer = io.BytesIO()
        image.save(buffer, format="ICO")  # 转换为ICO格式
        buffer = Image.open(buffer)
        icon = pystray.Icon("name", buffer, title="小鱼干综合工具", menu=(
            pystray.MenuItem('打开', show_window),
            pystray.MenuItem('退出', quit_window)
        ))

        icon.run()

    except Exception as e:
        print(f"无法创建托盘图标: {e}")


# 创建Tkinter应用
root = tk.Tk()
root.title("Simple Tkinter App")
root.geometry("300x200")  # 设置窗口大小
# 设置关闭按钮的行为为最小化到托盘而不是退出程序
root.protocol('WM_DELETE_WINDOW', withdraw_window)
# root.protocol("WM_RBUTTONDBLCLK", show_window)
# 运行Tkinter主循环
root.mainloop()
