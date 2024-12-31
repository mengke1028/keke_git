import tkinter as tk
from tkinter import ttk
import win32gui
import win32con
import win32api
import pywintypes


# 回调函数，用于枚举所有窗口并收集标题、句柄和类名信息，同时根据类名进行过滤
def enum_windows_callback(hwnd, result_list):
    class_name = win32gui.GetClassName(hwnd)
    title = win32gui.GetWindowText(hwnd)
    if "ChatWnd" in class_name:  # 根据微信窗口的类名进行过滤，这里类名可能因微信版本等因素略有不同
        result_list.append((hwnd, title, class_name))
    return True


# 获取全部窗口的标题、句柄和类名信息，并按类名过滤出微信窗口相关信息
def get_wechat_windows_info():
    windows_info = []
    win32gui.EnumWindows(enum_windows_callback, windows_info)
    return windows_info


# 获取全部窗口的标题、句柄和类名信息，并按类名过滤出微信窗口相关信息
def get_wechat_windows_info():
    windows_info = []
    win32gui.EnumWindows(enum_windows_callback, windows_info)
    return windows_info


# 创建主窗口UI
def create_ui():
    global window_combobox, transparency_entry
    root = tk.Tk()
    root.title("小鱼干")
    root.geometry("300x150")

    # 选择窗口标签及下拉菜单
    window_label = tk.Label(root, text="选择微信窗口")
    window_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
    window_combobox = ttk.Combobox(root, width=20)
    window_combobox.grid(row=0, column=1, padx=10, pady=5)
    # 绑定下拉菜单的点击事件，点击时触发更新函数
    window_combobox.bind("<Button-1>", lambda event: update_window_combobox())

    # 设置透明度标签及数字输入框
    transparency_label = tk.Label(root, text="设置透明度")
    transparency_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
    transparency_entry = tk.Entry(root, width=22)
    transparency_entry.insert(tk.INSERT, "50")  # 默认值设为 50
    transparency_entry.grid(row=1, column=1, padx=10, pady=10)

    # 开始按钮
    start_button = tk.Button(root, text="开始", command=lambda: start_operation(), width=30)
    start_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
    start_button.config(bg='green')
    # 初始化窗口下拉菜单的值

    root.mainloop()


# 更新窗口下拉菜单的选项
def update_window_combobox():
    wechat_windows_info = get_wechat_windows_info()
    window_names = [title for _, title, _ in wechat_windows_info]
    window_combobox['values'] = window_names
    if window_names:  # 如果有窗口信息，设置默认选中第一个
        window_combobox.set(window_names[0])

# 开始按钮点击后的操作
def start_operation():
    selected_window_index = window_combobox.current()
    selected_window_info = get_wechat_windows_info()[selected_window_index]
    handle = selected_window_info[0]
    transparency = int(transparency_entry.get())
    # 这里可以添加后续利用窗口句柄和透明度进行实际操作的代码，比如设置窗口透明度等
    set_window_transparency(handle, transparency)


def set_window_transparency(hwnd, transparency):
    """
    设置指定窗口的透明度。
    :param hwnd: 窗口句柄
    :param transparency: 透明度百分比（0 - 100）
    """
    # 检查透明度参数值范围是否合法
    if transparency < 0 or transparency > 100:
        raise ValueError("透明度百分比参数必须在0 - 100之间")
    alpha_value = transparency * 255 // 100
    alpha_value = max(0, min(255, alpha_value))  # 确保alpha值在0 - 255之间

    # 添加WS_EX_LAYERED样式，使窗口支持分层属性，以便设置透明度
    window_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    window_style |= win32con.WS_EX_LAYERED
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, window_style)

    # 设置层叠窗口的扩展样式相关参数
    layered_extended_style = 0x00080000
    lwa_alpha = 0x00000002
    transparent_color = 0

    try:
        win32gui.SetLayeredWindowAttributes(hwnd, transparent_color, alpha_value, lwa_alpha)
    except pywintypes.error as e:
        print(f"设置窗口透明度出现错误: {e}")


if __name__ == "__main__":
    wechat_windows_info = get_wechat_windows_info()
    for handle, title, class_name in wechat_windows_info:
        print(f"窗口句柄: {handle}, 窗口标题: {title}, 类名: {class_name}")

    create_ui()
