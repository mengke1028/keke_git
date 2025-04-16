# -*- coding: utf-8 -*-
# Keke.Meng  2025/1/7 10:45
import tkinter as tk
from tkinter import ttk
import win32con
import pywintypes
import win32gui


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


def callback():
    window_title = win32gui.FindWindow(None, '雷电模拟器(64)')
    window_title = win32gui.FindWindow(None, 'Microsoft Edge')
    print(window_title)
    return window_title


import win32gui


def get_edge_window_handle(leiming):
    def callback(hwnd, hwnds):
        # 获取窗口的标题
        window_title = win32gui.GetWindowText(hwnd)
        # print(window_title)
        # 获取窗口的类名
        window_class = win32gui.GetClassName(hwnd)
        # 检查类名是否为 "Chrome_WidgetWin_1"（Edge 浏览器的类名）
        if leiming == window_title:
            hwnds.append(hwnd)
        return True

    hwnds = []
    # 枚举所有顶级窗口
    win32gui.EnumWindows(callback, hwnds)
    return hwnds


if __name__ == '__main__':
    # # 调用函数获取 Edge 窗口句柄
    leiming = '196 836 990 2'
    edge_handles = get_edge_window_handle(leiming)
    if edge_handles:
        print(f"找到 {leiming}窗口句柄:")
        for handle in edge_handles:
            print(handle)
            # set_window_transparency(handle, 5)
    else:
        print("未找到 Microsoft Edge 窗口。")

    # window_title = callback()
    # set_window_transparency(595236, 60)
