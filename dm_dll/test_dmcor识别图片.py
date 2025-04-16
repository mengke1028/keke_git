# # -*- coding: utf-8 -*-
# # Keke.Meng  2025/3/14 13:52
# import ctypes
# import os
# import socket
# import sys
#
# import win32com.client
#
# patch = ctypes.windll.LoadLibrary(r'D:\keke\dm_dll\momoreg.dll')
# patch.SetDllPathW(r'D:\keke\dm_dll\momo.dll', 0)
#
# dm = win32com.client.Dispatch('dm.dmsoft')  # 调用大漠插件,获取大漠对象
# dm.setDict(0,  r'D:\keke\dm_dll\MK字库_1.txt')
# dm.useDict(0)
# dmversion = dm.Ver()
# print(dmversion)
# x1, y1, x2, y2 = 552, 126, 663, 194
# file_name = r'D:\keke\dm_dll\test.bmp'
# color = "ff3132-222222"
# result = dm.OcrInFile(x1, y1, x2, y2, file_name, color, 1.0)
# print(result)

from PIL import Image
import numpy as np


def read_bmp_to_array(file_path):
    try:
        # 打开BMP图片
        image = Image.open(file_path)
        # 将图片转换为NumPy数组
        image_array = np.array(image)
        return image_array
    except Exception as e:
        print(f"读取图片时出现错误: {e}")
        return None


def save_array_to_bmp(image_array, output_path):
    try:
        # 将NumPy数组转换回PIL图像对象
        image = Image.fromarray(image_array)
        # 保存为BMP格式图片
        image.save(output_path, 'BMP')
        print(f"图片已成功保存到 {output_path}")
    except Exception as e:
        print(f"保存图片时出现错误: {e}")


# 示例用法
image_path = 'D:/keke/dm_dll/test.bmp'

image_array = read_bmp_to_array(image_path)
if image_array is not None:
    print("图片数组的内容:", image_array)

if image_array is not None:
    output_path = "2.bmp"
    save_array_to_bmp(image_array, output_path)
