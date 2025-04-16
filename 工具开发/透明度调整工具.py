import tkinter as tk
from tkinter import ttk
import win32gui
import win32con


def get_window_names():
    window_info = []

    def enum_windows_callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if window_text:
                window_info.append((hwnd, window_text))

    win32gui.EnumWindows(enum_windows_callback, None)
    return window_info


def show_window_handle(*args):
    selected_name = window_var.get()
    for hwnd, name in window_info:
        if name == selected_name:
            handle_entry.delete(0, tk.END)
            handle_entry.insert(0, str(hwnd))
            break


def adjust_dropdown_and_refresh():
    global window_info, window_names
    # 重新获取窗口信息
    window_info = get_window_names()
    window_names = [name for _, name in window_info]
    # 计算最大窗口名长度
    max_length = max([len(name) for name in window_names], default=0)
    # 更新下拉菜单选项
    window_menu['values'] = window_names
    window_menu['width'] = max_length + 2
    # 调整下拉列表高度
    num_items = len(window_names)
    window_menu['height'] = min(num_items, 15)


def set_window_transparency(transparency):
    selected_name = window_var.get()
    for hwnd, name in window_info:
        if name == selected_name:
            # 将透明度值转换到 0 - 255 范围
            alpha = int((int(transparency) / 100) * 255)
            try:
                # 设置窗口样式以支持透明度
                win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
                # 设置窗口透明度
                win32gui.SetLayeredWindowAttributes(hwnd, 0, alpha, win32con.LWA_ALPHA)
            except Exception as e:
                print(f"设置窗口透明度时出错: {e}")
            break


root = tk.Tk()
root.title("摸鱼神器-修改窗口透明度")

# 初始化窗口信息
window_info = get_window_names()
window_names = [name for _, name in window_info]

# 计算最大窗口名长度
max_length = max([len(name) for name in window_names], default=0)

# 创建下拉菜单
window_var = tk.StringVar(root)
if window_names:
    window_var.set(window_names[0])
else:
    window_var.set("未找到窗口")

# 设置下拉菜单宽度
window_menu = ttk.Combobox(root, textvariable=window_var, values=window_names, width=max_length + 2)
window_menu.pack(pady=20)
window_var.trace("w", show_window_handle)

# 调整下拉列表高度并在点击时重新获取窗口信息
window_menu['postcommand'] = adjust_dropdown_and_refresh

# 创建显示窗口句柄的输入框
handle_label = tk.Label(root, text="窗口句柄:")
handle_label.pack()
handle_entry = tk.Entry(root)
handle_entry.pack(pady=10)

# 初始化显示第一个窗口的句柄
if window_info:
    handle_entry.insert(0, str(window_info[0][0]))

# 创建透明度滑动条
transparency_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL,
                              label="透明度 (0 - 100)", command=set_window_transparency)
transparency_scale.set(100)  # 默认设置为不透明
transparency_scale.pack(pady=10)
handle_label = tk.Label(root, text="开发者Q 193904974")
handle_label.pack()
root.mainloop()
