import ctypes
import sys
import win32com.client
import win32com
import win32gui
from PIL import Image
from libs222.move_to import get_mater, set_XY
from libs222.点击在游戏生效 import click, direct_dic
from libs222.实现移动 import key_press, PressKey, ReleaseKey
import os
import cv2
import mss.tools
import numpy as np
import time
import mss

path = os.path.dirname(os.path.abspath(sys.argv[0]))
xpos = 0
ypos = 0
width = 800
length = 600
sct = mss.mss()
txt = path + r'\MK字库_2.txt'
f = open(txt, 'r', encoding='GBK')


def mk_OCR(x1, y1, x2, y2, colors, thd):
    """文字识别"""
    DIict = {}
    # 获取字点阵
    text = f.read()
    lines = text.splitlines()
    for line in lines:
        try:
            words = line.split("$")
            if words:
                bin_str = ""
                for word in words[0]:
                    for char in word:
                        # 将每个十六进制字符转换成一个二进制字符串，并填充到4位长度
                        byte = int(char, 16)
                        byte_bin = bin(byte)[2:].zfill(4)  # 每个十六进制字符对应的二进制字符串
                        bin_str += byte_bin

                # 任选一种长度，计算某种长度的整数倍
                m = len(bin_str) // 11  # 这里的11是举例，你可以替换成你需要的长度

                # bin_str = '000'
                # byte = int(words[0], 16)
                # byte_bin = bin(byte)[2:].zfill(4)
                # print(byte_bin)
                # bin_str += byte_bin
                # m = len(bin_str) // 11
                if (m % 4):
                    bin_str = bin_str[:-(m % 4)]
                arr = np.array([list(bin_str[i:i + 11].zfill(11)) for i in range(0, len(bin_str), 11)],
                               dtype=np.float32)
                arr = arr.transpose()  # 做成一个数字矩阵

                DIict[words[1]] = arr
        except:
            pass
    f.seek(0)
    img = sct.grab((x1, y1, x2, y2))
    pil_img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")

    color_list = colors.split('|')

    for color in color_list:
        r1 = int(color[0:2], 16)
        g1 = int(color[2:4], 16)
        b1 = int(color[4:6], 16)
        np_img = np.array(pil_img)

        empty_array = np.zeros_like(np_img)

        condition = (np_img[:, :, 0] == r1) & (np_img[:, :, 1] == g1) & (np_img[:, :, 2] == b1)
        empty_array[condition] = [255, 255, 255]
        empty_array[~condition] = [0, 0, 0]
        # cv2.imshow('13', empty_array)
        # cv2.waitKey(0)
        pil_img = Image.fromarray(empty_array)
        cv_img = cv2.cvtColor(np.array(pil_img, dtype=np.float32), cv2.COLOR_BGR2RGB)  # PIL 转 OPCV
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

        matching_keys = []  # 存储符合条件的键值
        for k, v in DIict.items():

            result = cv2.matchTemplate(v, cv_img, 3)
            locations = np.where(result >= thd)  # 找到满足条件的位置
            if len(locations[0]) > 0:
                row_indices, col_indices = locations
                for row, col in zip(row_indices, col_indices):
                    matching_keys.append(((row, col), k))
        sorted_keys = sorted(matching_keys, key=lambda item: item[0][1])  # 按照 x 坐标从左到右排序
        sorted_keys = [k for _, k in sorted_keys]  # 提取键值
        sorted_keys_str = ''.join(sorted_keys)
        return sorted_keys_str
    return -1


def FindString(x1, y1, x2, y2, str1, colors, thd):
    """找字"""
    des = None
    # 获取字点阵
    text = f.read()

    lines = text.splitlines()
    for line in lines:
        try:
            words = line.split("$")
            if words:
                if str1 == words[1]:
                    des = words[0]
        except:
            continue
    f.seek(0)
    if des:
        pass
    else:
        print('字库不存在该点阵')
        return -1

    bin_str = ''

    for c in des:
        byte = int(c, 16)
        byte_bin = bin(byte)[2:].zfill(4)
        bin_str += byte_bin
    m = len(bin_str) // 11
    if (m % 4):
        bin_str = bin_str[:-(m % 4)]
    arr = np.array([list(bin_str[i:i + 11]) for i in range(0, len(bin_str), 11)], dtype=np.float32)
    arr = arr.transpose()  # 做成一个数字矩阵
    # 获取二值化图像点阵
    # 从内存中读取图像
    img = sct.grab((x1, y1, x2, y2))
    pil_img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")

    color_list = colors.split('|')
    for color in color_list:
        r1 = int(color[0:2], 16)
        g1 = int(color[2:4], 16)
        b1 = int(color[4:6], 16)
        np_img = np.array(pil_img)

        empty_array = np.zeros_like(np_img)

        condition = (np_img[:, :, 0] == r1) & (np_img[:, :, 1] == g1) & (np_img[:, :, 2] == b1)
        empty_array[condition] = [255, 255, 255]
        empty_array[~condition] = [0, 0, 0]

        pil_img = Image.fromarray(empty_array)
        cv_img = cv2.cvtColor(np.array(pil_img, dtype=np.float32), cv2.COLOR_BGR2RGB)  # PIL 转 OPCV

        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        p0 = 0, 0
        result = cv2.matchTemplate(arr, cv_img, 3)
        loc = np.where(result >= thd)
        ls = []
        for pt in zip(*loc[::-1]):  # Switch columns and rows
            if not abs(p0[0] - pt[0]) <= 14 and abs(p0[1] - pt[1]) > 14:
                p0 = pt
                # print(pt)
                top_left = pt[0], pt[1]
                ls.append(top_left)
        if len(ls) > 0:
            sorted_coordinates = sorted(ls, key=lambda x: x[0])  # 按照X坐标排序，返回第一个坐标
            return sorted_coordinates[0]
        else:
            return -1
    return -1


def find_image_in_region2(x1, y1, x2, y2, template, similarity_threshold, fangshi=3):
    """找图"""

    monitor = {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}
    screenshot = sct.grab(monitor)
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.IMREAD_COLOR)
    # 提取感兴趣的区域
    # roi = screenshot[y1:y2, x1:x2]
    #
    # cv2.imshow("image", roi)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 转换模板图像和输入图像的数据类型为CV_8U
    found_locations = template.split("|")
    ls = []
    try:
        for i, template_path in enumerate(found_locations):
            template = cv2.imdecode(np.fromfile(file=template_path), cv2.IMREAD_COLOR)
            template = cv2.cvtColor(template, cv2.IMREAD_COLOR)

            roi = cv2.cvtColor(screenshot, cv2.IMREAD_COLOR)
            # 进行模板匹配
            result = cv2.matchTemplate(roi, template, fangshi)
            # 设定阈值
            threshold = similarity_threshold
            loc = np.where(result >= threshold)
            # 在原图上标记匹配的位置
            p0 = 0, 0
            for pt in zip(*loc[::-1]):  # Switch columns and rows
                if not abs(p0[0] - pt[0]) <= 30 and abs(p0[1] - pt[1]) > 4:
                    p0 = pt
                    top_left = pt[0], pt[1]
                    ls.append(top_left)
            if len(ls) > 0:
                return ls
            else:
                return -1

    except Exception as e:
        print('报错', e)
    return -1


def find_image_in_region(x1, y1, x2, y2, template2, similarity_threshold, fangshi=3):
    """再区域内找到1张图"""
    quyu =  [
        (0,0,400,300),
        (0,300,400,600),
        (400, 0, 800, 300),
        (400, 300, 800, 600),
    ]
    for qy in quyu:
        (x1, y1, x2, y2) = qy
        monitor = {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}
        screenshot = sct.grab(monitor)
        screenshot = np.array(screenshot)
        screenshot = cv2.cvtColor(screenshot, cv2.IMREAD_COLOR)
        # 提取感兴趣的区域
        # roi = screenshot[y1:y2, x1:x2]
        #
        # cv2.imshow("image", roi)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # 转换模板图像和输入图像的数据类型为CV_8U
        found_locations = template2.split("|")
        try:
            for i, template_path in enumerate(found_locations):
                t2 = time.time()
                template = cv2.imdecode(np.fromfile(file=template_path), cv2.IMREAD_COLOR)
                template = cv2.cvtColor(template, cv2.IMREAD_COLOR)

                roi = cv2.cvtColor(screenshot, cv2.IMREAD_COLOR)
                # 进行模板匹配
                result = cv2.matchTemplate(roi, template, fangshi)

                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                # 判断相似度是否超过阈值
                if max_val >= similarity_threshold:
                    # 计算找到的图像在屏幕上的左上角坐标
                    top_left = i, max_loc[0] + x1, max_loc[1] + y1
                    return top_left
                else:
                    pass
        except Exception as e:
            print('报错', e)
    return -1


if __name__ == '__main__':
    for i in range(50):
        t = time.time()
        res = find_image_in_region(0, 0, 800, 600, r'C:\Users\小鱼干\Desktop\dnf2\DNF_RUNG2全职业_非大漠\IMG\基础达标.bmp', 0.99, 3)
        print((time.time() -t )*1000,'ms')
