# -*- coding: utf-8 -*-
# Keke.Meng  2025/1/7 10:45
import tkinter as tk
from tkinter import ttk
import win32gui
import win32con
import win32api
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
    print(window_title)
    return window_title


if __name__ == '__main__':
    window_title = callback()

    set_window_transparency(window_title, 5)
