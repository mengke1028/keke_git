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
    try:
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
        # # 将 PIL 图像转换为 OpenCV 格式
        # opencv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        # 将 OpenCV 图像转换为灰度图像
        opencv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        cv2.imshow('13', opencv_img)
        cv2.waitKey(0)

        color_list = [tuple(int(color[i:i + 2], 16) for i in (4, 2, 0)) for color in colors.split('|')]
        # colors_to_keep = [(0xc8, 0xc8, 0xc8), (0xc7, 0xc7, 0xc7), (0xc9, 0xc9, 0xc9)]
        mask = np.zeros_like(opencv_img[:, :, 0], dtype=np.bool_)
        for color in color_list:
            # 计算颜色的差异阈值
            lower_bound = np.array(color) - 5  # 允许一些小的偏差
            upper_bound = np.array(color) + 5  # 允许一些小的偏差

            # 创建颜色范围的掩码
            color_mask = cv2.inRange(opencv_img, lower_bound, upper_bound)

            # 更新总掩码
            mask = mask | (color_mask > 0)
        opencv_img[~mask] = [0, 0, 0]

        pil_img = Image.fromarray(opencv_img)
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
    except Exception as e:
        print(e)
        return -1


def FindString(x1, y1, x2, y2, str1, colors, thd):
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
        return -1, -1

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
    pil_img1 = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")


    # 将 PIL 图像转换为 NumPy 数组
    img_array = np.array(pil_img1)

    # 将 OpenCV 图像转换为灰度图像
    gray_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

    output_image = np.zeros_like(gray_img)

    # target_color = [tuple(int(color[i:i + 2], 16) for i in (4, 2, 0)) for color in colors.split('|')]
    # 创建一个掩膜，查找与目标颜色相同的像素
    # 定义要保留的灰度值（153 和 154）
    target_gray_values = colors

    # 创建一个掩膜，查找与目标灰度值相同的像素
    mask = np.isin(gray_img, target_gray_values)

    output_image[mask] = gray_img[mask]

    pil_img = Image.fromarray(output_image)
    cv_img = cv2.cvtColor(np.array(pil_img, dtype=np.float32), cv2.COLOR_BGR2RGB)  # PIL 转 OPCV

    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('13', cv_img)
    # cv2.waitKey(0)
    result = cv2.matchTemplate(arr, cv_img, 3)
    minv, maxv, minl, maxl = cv2.minMaxLoc(result)
    if maxv < thd:
        pass
    else:
        return maxl[0] + x1, maxl[1] + y1
    return -1


def Find_SS_String(x1, y1, x2, y2):
    """查找SS"""
    img = sct.grab((x1, y1, x2, y2))
    pil_img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
    color = 'ffb400'
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

    color_threshold = np.array([255, 255, 255])
    white_pixels = np.where(np.all(cv_img == color_threshold, axis=-1))

    # white_pixels是一个元组，其中包含两个numpy数组，分别对应满足条件的像素的y坐标和x坐标
    # 我们可以转换它们为一个坐标列表
    coordinates = list(zip(white_pixels[0], white_pixels[1]))
    coordinates.sort(key=lambda x: (x[0], x[1]))

    # 打印所有的白色像素坐标
    ss_list = []
    for coord in coordinates:
        ss_list.append((coord[1], coord[0]))

        # return
        # print(int(coord[0])+x1)
        # print(int(coord[1])+y1)
        # X = int(coord[0])+x1
        # Y = int(coord[1])+y1
        # print((X,Y))
        # print(((int(coord[0])+x1), int(color[1])+y1))
    if len(ss_list) > 0:
        # X = int((int(ss_list[0][0]) + ss_list[-1][0]) / 2) + x1
        # Y = int((int(ss_list[-1][1]) + ss_list[-1][1]) / 2) + y1
        X = int(ss_list[0][0]) + x1
        Y = int(ss_list[-1][1]) + y1

        return X, Y
    else:
        return -1


def find_image_in_region(x1, y1, x2, y2, template, similarity_threshold, fangshi=3):
    """获取屏幕截图"""
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
    try:
        for i, template_path in enumerate(found_locations):
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
        print(e)
    return -1


def find_image_in_region2(x1, y1, x2, y2, template, similarity_threshold, fangshi=3):
    """获取屏幕截图"""
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
    try:
        for i, template_path in enumerate(found_locations):
            template = cv2.imdecode(np.fromfile(file=template_path), cv2.IMREAD_COLOR)
            template = cv2.cvtColor(template, cv2.IMREAD_COLOR)

            roi = cv2.cvtColor(screenshot, cv2.IMREAD_COLOR)
            # 进行模板匹配
            result = cv2.matchTemplate(roi, template, fangshi)
            # 设定阈值
            threshold = similarity_threshold
            step_x, step_y = 30, 4  # 宽度步长为30，高度步长为4
            loc = np.where(result >= threshold)
            # 在原图上标记匹配的位置
            p0 = 0, 0
            # matched_positions = list(zip(*loc[::-1]))  # 转换为(x, y)格式
            #
            # return matched_positions
            ls = []
            for pt in zip(*loc[::-1]):  # Switch columns and rows
                if not abs(p0[0] - pt[0]) <= 30 and abs(p0[1] - pt[1]) > 4:
                    p0 = pt
                    # print(pt)
                    top_left = pt[0], pt[1]
                    ls.append(top_left)
            if len(ls) > 0:
                return ls
            else:
                return -1

    except Exception as e:
        print('报错', e)
    return -1


def INIT_all():
    """初始化窗口"""
    CK = win32gui.FindWindow("地下城与勇士", "地下城与勇士：创新世纪")
    win32gui.SetForegroundWindow(CK)
    xpos = 0
    ypos = 0
    width = 800
    length = 600
    win32gui.MoveWindow(CK, xpos, ypos, width, length, True)


def get_tiaoguo():
    """找图-翻牌跳过"""
    resp = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\ESC.bmp", 0.98)
    if resp != -1:
        print(resp)
        print("找到", 'ESC')
        return True


def get_weishiqu():
    """找到SS"""
    return

    resp = find_image_in_region(237, 189, 578, 297, path + r"\IMG\存在ss.bmp", '000000-000000', 0.8, 0)
    if resp[0] == '0':
        time.sleep(3)
        return True


def get_xiuli(dm):
    """找图-翻牌跳过"""
    xiuli = dm.FindStrFastE(343, 248, 640, 454, "确定要修理吗", "ffffff-000000", 1)
    if "-1" in xiuli:
        print("没找到 <修理>")
        return False
    else:
        print("找到 <修理>")
        return True


def get_PL():
    """读取当前PL值"""
    for i in range(10):
        res = mk_OCR(676, 555, 807, 633, "c8c8c8|c7c7c7|c9c9c9", 0.99)
        print(res)
        res = res.split('/')[0].split('：')[-1]
        print('疲劳值：', res)
        try:
            return int(res)
        except Exception as E:
            print(E)
            time.sleep(1)
    return None
    #     if res == "":
    #         if Find_exit(dm):
    #             key_press("ESC")
    #         click(724, 592)  # 移动到PL位置
    #         dm.setDict(0, path + r'\MK字库_2.txt')
    #         time.sleep(3)
    #         print('重新加载字库')
    #     data = "".join(list(filter(str.isdigit, res))).replace(' ', '')
    #     print("当前疲劳值为：", data[:-3])
    #     print("识别耗时",time.time() -t)
    #     return int(data[:-3])
    # except:
    #     time.sleep(1)
    #     pass


def find_use_png(x1, y1, x2, y2, template, similarity_threshold, fangshi=3):
    """获取屏幕截图"""
    img = sct.grab((x1, y1, x2, y2))
    pil_img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
    # 将 OpenCV 图像转换为灰度图像
    opencv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    gray_opencv_img = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2GRAY)

    colors = 'feff00|fffe01|ffff00|fffe00|ffff01'
    color_list = [tuple(int(color[i:i + 2], 16) for i in (4, 2, 0)) for color in colors.split('|')]
    # colors_to_keep = [(0xc8, 0xc8, 0xc8), (0xc7, 0xc7, 0xc7), (0xc9, 0xc9, 0xc9)]
    mask = np.zeros_like(gray_opencv_img, dtype=np.bool_)
    for color in color_list:
        # 计算颜色的差异阈值
        lower_bound = np.array(color)  # 允许一些小的偏差
        upper_bound = np.array(color)  # 允许一些小的偏差

        # 创建颜色范围的掩码
        color_mask = cv2.inRange(opencv_img, lower_bound, upper_bound)

        # 更新总掩码
        mask = mask | (color_mask > 0)
    opencv_img[~mask] = [0, 0, 0]
    # cv2.imshow('13', opencv_img)
    # cv2.waitKey(0)
    # 转换模板图像和输入图像的数据类型为CV_8U
    found_locations = template.split("|")
    try:
        for i, template_path in enumerate(found_locations):
            template = cv2.imdecode(np.fromfile(file=template_path), cv2.IMREAD_COLOR)
            template = cv2.cvtColor(template, cv2.IMREAD_COLOR)

            # cv2.imshow('13', opencv_img)
            # cv2.waitKey(0)
            result = cv2.matchTemplate(opencv_img, template, fangshi)
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


def Find_use(shengao=133):
    """定位角色位置,返回角色当前坐标"""
    resp_mxt = find_use_png(0, 145, 800, 529, path + r"\IMG\基础达标.bmp", 0.99)
    try:
        if resp_mxt != -1:
            X = resp_mxt[1]
            Y = resp_mxt[2]
            return int(X) + 23, int(Y) + shengao
        return None
    except:
        print(resp_mxt)


def get_shengao():
    """判断身高"""
    resp_mxt = find_use_png(xpos, ypos, width, length, path + r"\IMG\基础达标.bmp", 0.99)
    if resp_mxt != -1:
        Y = resp_mxt[2]
        shengao = 417 - int(Y)
        print('身高：', shengao)
        return shengao
    else:
        return 133


def Find_monster():
    """定位角色位置,返回角色当前坐标"""
    resp_mxt = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\怪物.bmp", 0.99)
    if resp_mxt != -1:
        print("找到怪物")
        X = resp_mxt[1]
        Y = resp_mxt[2]
        return int(X) + 10, int(Y) + 50
    else:
        print("没有怪物")
    return None


def Find_5tu(img):
    """定位5图的坐标"""
    resp_mxt = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\{}".format(img), 0.9)
    if resp_mxt != -1:
        X = resp_mxt[1]
        Y = resp_mxt[2]
        if img == "摇篮5图.bmp":
            return int(X) + 60, int(Y) + 138 + 61
        elif img == "摇篮2图.bmp":
            return int(X) - 68, int(Y) + 35
        elif img == "迷雾高原图1.bmp":
            return int(X) - 100, int(Y) + 246
        elif img == "迷雾高原图2.bmp":
            return int(X) + 227, int(Y) + 292
        elif img == "迷雾高原图3.bmp":
            return int(X) + 302, int(Y) + 144
        elif img == "迷雾高原图4.bmp":
            return int(X) + 57, int(Y) + 197
        elif img == "迷雾高原图5.bmp":
            return int(X) + 211, int(Y) + 319
        elif img == "迷雾高原图6.bmp":
            return int(X) + 101, int(Y) + 227
        elif img == "迷雾高原图7.bmp":
            return int(X) + 149, int(Y) + 305
    else:
        return None


def Find_men2(img='门.bmp'):
    """查找门坐标"""
    resp_mxt1 = find_image_in_region2(xpos, ypos, width, length, path + r"\IMG\门.bmp", 0.99, 3)
    if resp_mxt1 != -1:
        X = resp_mxt1[-2]
        Y = resp_mxt1[-1]
        return int(X), int(Y)

    resp_mxt = find_image_in_region2(xpos, ypos, width, length, path + r"\IMG\{}".format('摇篮5图.bmp'), 0.9)
    if resp_mxt != -1:
        X = resp_mxt[-2]
        Y = resp_mxt[-1]
        return int(X) + 60, int(Y) + 138 + 61

    else:
        print('没找门')
        return None


def Find_men3(xpos=0, ypos=0, width=800, length=600, img='门.bmp'):
    """查找门坐标"""
    resp_mxt1 = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\门1.bmp|" + path + r"\IMG\门_海伯伦.bmp", 0.99,
                                     3)
    if resp_mxt1 != -1:
        print('有门', resp_mxt1)
        X = resp_mxt1[-2]
        Y = resp_mxt1[-1]
        return int(X), int(Y)
    else:
        print('没找到门')
        return None


def Find_men4(paixu=0):
    """查找门坐标
    paixu == 0  按照X排序
    paixu == 1 按照Y排序
    """

    resp_mxt1 = find_image_in_region2(xpos, ypos, width, length, path + r"\IMG\门1.bmp|" + path + r"\IMG\门_海伯伦.bmp",
                                      0.99, 3)
    print(resp_mxt1)
    if resp_mxt1 != -1:
        if paixu in [0, 1]:
            sorted_coordinates = sorted(resp_mxt1, key=lambda x: x[paixu])
        elif paixu in [2]:
            sorted_coordinates = sorted(resp_mxt1, key=lambda x: x[1], reverse=True)  # Y 轴反向排序
        else:
            sorted_coordinates = sorted(resp_mxt1, key=lambda x: x[0])

        resp = sorted_coordinates[0]
        print('有门', resp)
        X = resp[-2]
        Y = resp[-1]
        return int(X), int(Y)
    else:
        print('没找到门')
        return None


def Find_2tu(img):
    """定位2图的坐标"""
    time.sleep(0.1)
    resp_mxt = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\{}".format(img), 0.9)

    if resp_mxt != -1:
        X = resp_mxt[1]
        Y = resp_mxt[2]
        return int(X) - 68, int(Y) + 35
    else:
        return None


def Find_men(img='N'):
    """查找门坐标"""
    # resp_mxt = find_image_in_region(150, 213, 800, 599,
    #                                 path + r"\IMG\门2.bmp |" + path + r'\IMG\门3.bmp|' + path + r'\IMG\门1.bmp', 0.99)
    resp_mxt = find_image_in_region(221, 101, 797, 562,
                                    path + r"\IMG\门.bmp ", 0.98, 3)
    resp_mxt2 = find_image_in_region(221, 101, 797, 562,
                                     path + r'\IMG\门3.bmp', 0.95, 5)
    if resp_mxt != -1:
        print('发现门')
        X = resp_mxt[1]
        Y = resp_mxt[2]
        return int(X), int(Y)
    elif resp_mxt2 != -1:
        print('发现门')
        X = resp_mxt2[1]
        Y = resp_mxt2[2]
        return int(X), int(Y)
    else:
        print('没找到门')
        return None


def Find_men_SD(img='N'):
    """查找门坐标"""
    # resp_mxt = find_image_in_region(150, 213, 800, 599,
    #                                 path + r"\IMG\门2.bmp |" + path + r'\IMG\门3.bmp|' + path + r'\IMG\门1.bmp', 0.99)
    resp_mxt = find_image_in_region(145, 267, 798, 565,
                                    path + r"\IMG\门.bmp ", 0.98, 3)
    resp_mxt2 = find_image_in_region(145, 267, 798, 565,
                                     path + r'\IMG\门3.bmp', 0.95, 5)
    if resp_mxt != -1:
        print('发现门1')
        X = resp_mxt[1]
        Y = resp_mxt[2]
        return int(X), int(Y)
    elif resp_mxt2 != -1:
        print('发现门2')
        X = resp_mxt2[1]
        Y = resp_mxt2[2]
        return int(X), int(Y)
    else:
        print('没找到门')
        return None


def Find_exit():
    """打开菜单"""
    guanbi = FindString(690, 125, 718, 143, "关", "9f8950", 0.9)
    if guanbi != -1:
        print("找到 <关闭> 菜单关闭")
        return True
    else:
        print("没找到 <关闭> 菜单关闭")
        return False


def Find_open():
    """判断是否开门"""
    time1 = time.time() + 0.2
    while time1 > time.time():
        resp_mxt = find_image_in_region(733, 60, 799, 140,
                                        path + "\IMG\开门信号3.bmp|" + path + r"\IMG\开门信号.bmp|" + path + "\IMG\开门信号2.bmp",
                                        1, 5)
        if '-1' not in str(resp_mxt):
            print('门开了')
            return True
    return False


def Find_open2():
    """判断是否开门"""
    time1 = time.time() + 0.3
    while time1 > time.time():
        resp_mxt = find_image_in_region(699, 43, 794, 122,
                                        path + "\IMG\开门信号3.bmp|" + path + r"\IMG\开门信号.bmp|" + path + "\IMG\开门信号2.bmp|" + path + "\IMG\开门信号8.bmp|" + path + "\IMG\开门信号4.bmp",
                                        0.95, 5)
        if resp_mxt != -1:
            return True
    print('门没开')
    return False


def Find_open_SD():
    """判断是否开门"""
    time1 = time.time() + 0.5
    while time1 > time.time():
        resp_mxt = find_image_in_region(679, 50, 791, 89,
                                        path + "\IMG\圣殿开门1.bmp|" +
                                        path + r"\IMG\开门信号.bmp|" +
                                        path + "\IMG\开门信号2.bmp|" +
                                        path + "\IMG\开门信号7.bmp|" +
                                        path + "\IMG\圣殿开门2.bmp",
                                        1, 3)
        if resp_mxt != -1:
            return True
    print('门没开')
    return False


def Find_open_fengbao():
    """判断是否开门"""
    time1 = time.time() + 0.5
    while time1 > time.time():
        resp_mxt = find_image_in_region(693, 45, 794, 87,
                                        path + "\IMG\开门信号5.bmp|" +
                                        path + r"\IMG\开门信号.bmp|" +
                                        path + r"\IMG\开门信号11.bmp|" +
                                        path + r"\IMG\开门信号7.bmp|" +
                                        path + r"\IMG\开门信号10.bmp|" +
                                        path + r"\IMG\开门信号9.bmp|" +
                                        path + r"\IMG\开门信号12.bmp|" +
                                        path + "\IMG\开门信号2.bmp",
                                        0.999)

        if '-1' not in str(resp_mxt):
            print('开了')
            return True
    return False


def Find_open_jingjileyuan():
    """判断荆棘乐园"""
    time1 = time.time() + 0.5
    while time1 > time.time():
        resp_mxt = find_image_in_region(661, 51, 788, 107,
                                        path + r"\IMG\荆棘乐园开门信号1.bmp|" + path + r"\IMG\荆棘乐园开门信号2.bmp",
                                        0.999)

        if '-1' not in str(resp_mxt):
            print('荆棘乐园门开了')
            return True
    return False


def Find_open_fengbaoyoucheng():
    """判断是否开门"""
    time1 = time.time() + 0.5
    while time1 > time.time():
        resp_mxt = find_image_in_region(686, 48, 793, 102,
                                        path + "\IMG\开门信号5.bmp|" + path + r"\IMG\开门信号.bmp|" + path + r"\IMG\开门信号7.bmp|" + path + "\IMG\开门信号2.bmp",
                                        0.99)
        if '-1' not in str(resp_mxt):
            return True
    return False


def Find_open_miwu():
    """判断是否开门"""
    time1 = time.time() + 1
    while time1 > time.time():
        resp_mxt = find_image_in_region(664, 26, 798, 88,
                                        path + "\IMG\迷雾开门信号2.bmp|" + path + r"\IMG\迷雾开门信号.bmp|",
                                        1)

        if '-1' not in str(resp_mxt):
            print("门开了")
            return True
        else:
            print("还没开")
    else:
        return False


def Find_open_miwu1(dm):
    """随机深渊判断是否开门"""
    time1 = time.time() + 1
    while time1 > time.time():
        resp_mxt = find_image_in_region(664, 26, 798, 88,
                                        path + "\IMG\迷雾开门信号1.bmp|" + path + r"\IMG\迷雾开门信号1_1.bmp|",
                                        "000000",
                                        0.9, 3)

        if '-1' not in resp_mxt:
            print("门开了")
            return True
        else:
            print("还没开")
    else:
        return False


def Find_open_miwu2(dm):
    """判断是否开门"""
    time1 = time.time() + 2
    while time1 > time.time():
        resp_mxt = find_image_in_region(664, 26, 798, 88,
                                        path + "\IMG\迷雾开门信号2_1.bmp|" + path + r"\IMG\迷雾开门信号2_2.bmp|",
                                        "000000",
                                        0.9, 3)

        if '-1' not in resp_mxt:
            print("门开了")
            return True
        else:
            print("还没开,222222222222")
    else:
        return False


def Find_shenyuan(dm):
    """判断是否遇到深渊"""
    time1 = time.time() + 2
    while time1 > time.time():
        resp_mxt = find_image_in_region(664, 26, 798, 88, path + "\IMG\随机深渊.bmp|" + path, "000000", 0.9, 3)

        if '-1' not in resp_mxt:
            print("深渊")
            return True
        else:
            print("没有深渊")
    else:
        return False


def get_user_map():
    """通过地图判断角色在几号房间"""
    boss = find_image_in_region(682, 24, 793, 103, path + r"\IMG\boss房间.bmp", 1)
    print(boss)
    if boss[0] == 0:
        print("出现牛头")
        use_map = find_image_in_region(682, 24, 793, 103, path + r"\IMG\地图角色.bmp", 1)
        if use_map[0] == 0:
            print(use_map)
            X = int(use_map[1])
            Y = int(use_map[2])
            if X == 691 and Y == 74:
                print("角色在图1")
                return 1
            elif X == 709 and Y == 74:
                print("角色在图2")
                return 2
            elif X == 727 and Y == 74:
                print("角色在图3")
                return 3
            elif X == 745 and Y == 74:
                print("角色在图4")
                return 4
            elif X == 763 and Y == 74:
                print("角色在图5")
                return 5

        elif '-1' in use_map:
            boss2 = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\紧急事件后检测.bmp", "000000", 0.9, 1)
            print('boss2 :', boss2)
            if '-1' not in boss2:
                return 6
            jinjishijian = find_image_in_region(682, 24, 793, 103, path + r"\IMG\紧急事件.bmp", 0.89)
            if jinjishijian[0] == '0':
                print("紧急事件出现")
                return 7
    else:
        print("找不到boss房间")


def get_boos():
    """判断牛头还在不在"""
    boss = find_image_in_region(736, 22, 794, 138, path + r"\IMG\boss房间.bmp", .89)
    if boss != -1:
        return True
    else:
        time.sleep(0.5)
        boss = find_image_in_region(736, 22, 794, 138, path + r"\IMG\boss房间.bmp", .89)
        if boss == -1:
            print('boos 不在了')
            return False
        else:
            return True


def get_boos_miwu(dm):
    """判断牛头还在不在"""
    boss = find_image_in_region(665, 23, 796, 86, path + r"\IMG\迷雾BOSS校验.bmp", 0.89)
    if boss[0] == '0':
        return True
    else:
        return False


def get_user_map_YL():
    """通过地图判断角色在几号房间"""
    boss = find_image_in_region(736, 22, 794, 138, path + r"\IMG\boss房间.bmp", .89)
    if boss != -1:
        use_map = find_image_in_region(736, 22, 794, 138, path + r"\IMG\地图角色.bmp", 0.89)
        if use_map != -1:
            X = int(use_map[1])
            Y = int(use_map[2])
            if X == 763 and Y == 128:
                print("角色在图1")
                return 1
            elif X == 763 and Y == 110:
                print("角色在图2")
                return 2
            elif X == 741 and Y == 115:
                print("角色在图2")
                return 2

            elif X == 781 and Y == 110:
                print("角色在图3")
                return 3
            elif X == 781 and Y == 92:
                print("角色在图4")
                return 4
            elif X == 763 and Y == 92:
                print("角色在图5")
                return 5
            elif X == 763 and Y == 74:
                print("角色在图6")
                return 6

        elif use_map == -1:
            boss2 = find_image_in_region(116, 176, 782, 537, path + r"\IMG\王之摇篮boss.bmp", 0.95)
            if boss2 != -1:
                print("角色在boos房间")
                return 7
            jinjishijian = find_image_in_region(736, 45, 794, 138, path + r"\IMG\紧急事件.bmp", 0.89)
            if jinjishijian != -1:
                print("紧急事件出现")
                return 8
    else:
        return None


def get_user_map_HBL():
    """海伯伦通过地图判断角色在几号房间"""
    boss = find_image_in_region(699, 46, 797, 118, path + r"\IMG\boss房间.bmp", .89)
    if boss != -1:
        use_map = find_image_in_region(697, 50, 791, 129, path + r"\IMG\地图角色.bmp", 0.89)
        if use_map != -1:
            X = int(use_map[1])
            Y = int(use_map[2])
            if X == 723 and Y == 115:
                print("角色在图1")
                return 1
            elif X == 705 and Y == 97:
                print("角色在图1")
                return 1
            elif X == 723 and Y == 97:
                print("角色在图2")
                return 2
            elif X == 741 and Y == 115:
                print("角色在图2")
                return 2
            elif X == 727 and Y == 74:
                print("角色在图2.1")
                return 2.1
            elif X == 741 and Y == 97:
                print("角色在图3")
                return 3
            elif X == 759 and Y == 115:
                print("角色在图3")
                return 3

            elif X == 741 and Y == 79:
                print("角色在图4")
                return 4
            elif X == 759 and Y == 97:
                print("角色在图4")
                return 4

            elif X == 741 and Y == 61:
                print("角色在图5")
                return 5
            elif X == 759 and Y == 79:
                print("角色在图5")
                return 5

            elif X == 759 and Y == 61:
                print("角色在图6")
                return 6

            elif X == 777 and Y == 79:
                print("角色在图6")
                return 9

            elif X == 763 and Y == 74:
                print("角色在图6.1")
                return 6.1


        elif use_map == -1:
            lingzhu = FindString(0, 0, 800, 600, "领主", "ff00ff", 0.98)
            if lingzhu != -1:
                print("角色在boos房间")
                return 7
            jinjishijian = find_image_in_region(697, 50, 791, 129, path + r"\IMG\紧急事件.bmp", 0.89)
            if jinjishijian != -1:
                print("紧急事件出现")
                return 8
            elif jinjishijian == -1:
                boss2 = find_image_in_region(697, 50, 791, 129, path + r"\IMG\boss房间.bmp", .89)
                use_map2 = find_image_in_region(697, 50, 791, 129, path + r"\IMG\地图角色.bmp", 0.89)
                if boss2 != -1 and use_map2 == -1:
                    print("角色在boos房间")
                    return 7

    else:
        return None


def get_user_map_FBNL():
    """风暴逆鳞通过地图判断角色在几号房间"""
    boss = find_image_in_region(716, 43, 798, 68, path + r"\IMG\boss房间.bmp", 0.89)
    if boss != -1:
        use_map = find_image_in_region(698, 46, 796, 86, path + r"\IMG\地图角色.bmp", 0.9)
        print(use_map)
        if use_map != -1:
            X = int(use_map[-2])
            Y = int(use_map[-1])
            if X == 723 and Y == 61:
                print("角色在图1")
                return 1
            elif X == 741 and Y == 79:
                print("角色在图1.1")
                return 1

            elif X == 741 and Y == 61:
                print("角色在图2")
                return 2

            elif X == 759 and Y == 79:
                print("角色在图2.1")
                return 2

            elif X == 759 and Y == 61:
                print("角色在图3")
                return 3

            elif X == 777 and Y == 79:
                print("角色在图3.1")
                return 3

        elif use_map == -1:
            time.sleep(0.2)
            use_map2 = find_image_in_region(716, 43, 798, 68, path + r"\IMG\地图角色.bmp", 0.89)
            boss2 = find_image_in_region(716, 43, 798, 68, path + r"\IMG\boss房间.bmp", 0.89)
            if boss2 != -1 and use_map2 == -1:
                print("角色在boos房间")
                return 4

        else:
            return None


def get_user_map_WDKD():
    """无底坑道通过地图判断角色在几号房间"""
    boss = find_image_in_region(627, 25, 800, 71, path + r"\IMG\boss房间.bmp", 0.9)
    if boss != -1:
        shenyuuan = find_image_in_region(627, 25, 800, 71, path + r"\IMG\无底坑道深渊.bmp", 0.98)
        if shenyuuan == -1:
            pass
        else:
            return 10
        use_map = find_image_in_region(627, 25, 800, 71, path + r"\IMG\地图角色.bmp", 0.9)
        print(use_map)
        if use_map != -1:
            X = int(use_map[-2])
            Y = int(use_map[-1])
            if X == 637 and Y == 56:
                print("角色在图1")
                return 1
            elif X == 655 and Y == 56:
                print("角色在图2")
                return 2
            elif X == 673 and Y == 56:
                print("角色在图3")
                return 3
            elif X == 691 and Y == 56:
                print("角色在图4")
                return 4
            elif X == 709 and Y == 56:
                print("角色在图5")
                return 5
            elif X == 727 and Y == 56:
                print("角色在图6")
                return 6
            elif X == 745 and Y == 56:
                print("角色在图7")
                return 7
            elif X == 763 and Y == 56:
                print("角色在图8")
                return 8

        elif use_map == -1:
            print("角色在boos房间")
            return 9

        guotu = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\过图.bmp", 0.9)
        if guotu == -1:
            print("过图中")
            return 0
        else:
            return None


def get_user_map_JJLY():
    """荆棘乐园通过地图判断角色在几号房间"""
    boss = find_image_in_region(660, 51, 792, 107, path + r"\IMG\boss房间.bmp", 0.9)
    if boss != -1:
        use_map = find_image_in_region(660, 51, 792, 107, path + r"\IMG\地图角色.bmp", 0.9)
        if use_map != -1:
            X = int(use_map[-2])
            Y = int(use_map[-1])
            if X == 669 and Y == 61:
                print("角色在图1")
                return 1
            elif X == 687 and Y == 61:
                print("角色在图2")
                return 2
            elif X == 705 and Y == 61:
                print("角色在图3")
                return 3
            elif X == 705 and Y == 79:
                print("角色在图4")
                return 4
            elif X == 687 and Y == 79:
                print("角色在图5")
                return 5
            elif X == 687 and Y == 97:
                print("角色在图6")
                return 6
            elif X == 705 and Y == 97:
                print("角色在图7")
                return 7
            elif X == 723 and Y == 97:
                print("角色在图8")
                return 8
            elif X == 723 and Y == 79:
                print("角色在图9")
                return 9
            elif X == 741 and Y == 79:
                print("角色在图10")
                return 10
            elif X == 759 and Y == 79:
                print("角色在图11")
                return 11

        elif use_map == -1:
            print("角色在boos房间")
            return 12

        guotu = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\过图.bmp", 0.9)
        if guotu == -1:
            print("过图中")
            return 0
        else:
            return None


def get_user_map_MWGY(dm):
    """通过地图判断角色在几号房间"""
    boss = find_image_in_region(665, 23, 796, 86, path + r"\IMG\boss房间2.bmp", 0.89)
    if boss[0] == '0':
        use_map = find_image_in_region(665, 23, 796, 86, path + r"\IMG\地图角色.bmp", "000000", 0.7, 1)
        if use_map[0] == '0':
            use_map = use_map.split("|")
            X = int(use_map[1])
            Y = int(use_map[2])
            if X == 673 and Y == 56:
                print("角色在图1")
                return 1
            elif X == 673 and Y == 74:
                print("角色在图2")
                return 2
            elif X == 691 and Y == 74:
                print("角色在图3")
                return 3
            elif X == 709 and Y == 74:
                print("角色在图4")
                return 4
            elif X == 727 and Y == 74:
                print("角色在图5")
                return 5
            elif X == 745 and Y == 74:
                print("角色在图6")
                return 6
            elif X == 763 and Y == 74:
                print("角色在图7")
                return 7

        elif '-1' in use_map:
            jingyingg = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\迷雾精英怪房间.bmp", "000000", 0.9, 1)
            print(jingyingg)
            if jingyingg[0] == '0':
                jingyingg = jingyingg.split("|")
                X = int(jingyingg[1])
                Y = int(jingyingg[2])
                if X == 706 and Y == 67:
                    print("角色在精英怪房间")
                    return 4

    else:
        use_map = find_image_in_region(665, 23, 796, 86, path + r"\IMG\地图角色.bmp", "000000", 0.7, 1)
        print(use_map)
        if use_map[0] == '0':
            use_map = use_map.split("|")
            X = int(use_map[1])
            Y = int(use_map[2])
            if X == 781 and Y == 74:
                print("角色在BOSS房间")
                return 8
        else:
            guotu = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\过图.bmp", "000000", 1, 1)
            if guotu[0] == '0':
                print("过图中")
                return 0
            else:
                return None


def get_user_map_FBYC():
    """风暴通过地图判断角色在几号房间"""
    boss = find_image_in_region(684, 46, 794, 102, path + r"\IMG\boss房间.bmp", 0.89)
    if boss != -1:
        use_map = find_image_in_region(684, 46, 794, 102, path + r"\IMG\地图角色.bmp", 0.89)
        if use_map != -1:
            X = int(use_map[1])
            Y = int(use_map[2])
            if X == 691 and Y == 74:
                print("角色在图1")
                return 1
            elif X == 709 and Y == 74:
                print("角色在图2")
                return 2
            elif X == 727 and Y == 74:
                print("角色在图3")
                return 3
            elif X == 745 and Y == 74:
                print("角色在图4")
                return 4
            elif X == 763 and Y == 74:
                print("角色在图5")
                return 5
        elif use_map == -1:
            time.sleep(0.1)
            use_map2 = find_image_in_region(684, 46, 794, 102, path + r"\IMG\地图角色.bmp", 0.89)
            boss2 = find_image_in_region(684, 46, 794, 102, path + r"\IMG\boss房间.bmp", 0.89)
            if boss2 != -1 and use_map2 == -1:
                print("角色在boos房间")
                return 6

        guotu = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\过图.bmp", 0.89)
        if guotu != -1:
            print("过图中")
            return 0
        else:
            return None


def get_user_map_SD():
    """圣殿通过地图判断角色在几号房间"""
    boss = find_image_in_region(677, 47, 791, 89, path + r"\IMG\boss房间.bmp", 0.89)
    if boss != -1:
        use_map = find_image_in_region(677, 47, 791, 89, path + r"\IMG\地图角色.bmp", 0.89)
        use_map_1 = find_image_in_region(677, 47, 791, 89, path + r"\IMG\圣殿1图.bmp", 0.89)
        if use_map != -1:
            X = int(use_map[1])
            Y = int(use_map[2])
            if X == 687 and Y == 61:
                print("角色在图1")
                return 1
            elif X == 687 and Y == 79:
                print("角色在图1")
                return 1

            elif X == 705 and Y == 61:
                print("角色在图2")
                return 2
            elif X == 705 and Y == 79:
                print("角色在图2")
                return 2
            if use_map_1 == (0, 683, 54) and boss != (0, 772, 54):
                if X == 723 and Y == 61:
                    print("角色在图3")
                    return 3
                elif X == 723 and Y == 79:
                    print("角色在图4")
                    return 4
                elif X == 741 and Y == 79:
                    print("角色在图5")
                    return 5
            elif use_map_1 == (0, 683, 72) and boss != (0, 772, 54):
                if X == 723 and Y == 79:
                    print("角色在图3")
                    return 3
                elif X == 723 and Y == 61:
                    print("角色在图4")
                    return 4
                elif X == 741 and Y == 61:
                    print("角色在图5")
                    return 5
            elif X == 723 and Y == 61:
                print("角色在图3")
                return 3
            elif X == 741 and Y == 61:
                print("角色在图4")
                return 4

            elif X == 759 and Y == 61:
                print("角色在图5")
                return 5

        elif use_map == -1:
            jinjishijian = find_image_in_region(677, 47, 791, 89, path + r"\IMG\紧急事件.bmp", 0.89)
            if jinjishijian != -1:
                print("紧急事件出现")
                return 7
            else:
                print('boss 房间')
                return 6

        guotu = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\过图.bmp", "000000", 0.89)
        if guotu != -1:
            print("过图中")
            return 0
        else:
            return None


def get_shangdian():
    """寻找<出售>"""
    print("寻找出售")
    time1 = time.time() + 15
    while time1 > time.time():
        shangdian = FindString(107, 510, 152, 538, "出", "b99460", 0.98)
        if shangdian != -1:
            print("找到 <出售> ")
            return True
        else:
            print("没找到 <出售> ")
            time.sleep(1)
            continue
    return False


def get_shangdian2():
    """寻找<出售>"""

    shangdian = FindString(107, 510, 152, 538, "出", ([153, 154]), 0.98)
    if "-1" in str(shangdian):
        return False
    else:
        print("找到 <出售> ")
        return True


def get_use():
    """进入选择角色"""
    while True:
        print('切换角色')
        time.sleep(1)
        key_press("ESC")
        time.sleep(1)
        res = FindString(348, 493, 437, 533, "角", "d6c592", 0.98)
        print(res)
        if res != -1:
            X = int(res[0])
            Y = int(res[1])
            click(X + 10, Y - 5)
            break
        else:
            continue


def Fenjie_SS():
    """分解SS"""
    print("开始分解SS")
    time.sleep(1)
    key_press("0")
    time.sleep(1)
    time1 = time.time() + 10
    fenjie = None
    while time1 > time.time():
        fenjie = FindString(94, 75, 601, 515, "备", 'b99460', 0.99)
        print('fenjie', fenjie)
        if fenjie == -1:
            print("没找到 <装备分解> ")
            time.sleep(1)
            key_press("0")
            time.sleep(2)
            continue
        else:
            print("找到 <修理分解机> ")
            xiuli = FindString(94, 75, 601, 515, "机", "b99460", 0.98)
            if xiuli != -1:
                X = int(xiuli[-2])
                Y = int(xiuli[-1])
                time.sleep(1)
                click(X, Y)
                time.sleep(1)
                click(X, Y)
                time.sleep(1)
                key_press("SPACE")
            time.sleep(1)
            break
    if fenjie != -1:
        X = int(fenjie[-2])
        Y = int(fenjie[-1])
        time.sleep(1)
        click(X, Y)
        time.sleep(1)

        y = 326
        for i in range(2):
            x = 493
            for _ in range(8):
                click(x, y)
                x = x + 30
            y += 30
        click(1, 1)
        time.sleep(1)
        fenjie = FindString(94, 75, 601, 515, "分", "b99460", 0.9)
        if fenjie != -1:
            X = int(fenjie[-2])
            Y = int(fenjie[-1])
            click(X, Y)
            time.sleep(1)
            click(X, Y)
            time.sleep(5)
            key_press("ESC")

            return True
        else:
            key_press("ESC")
            return True


def move(k, timeout=0.5):
    """移动方向"""
    PressKey(direct_dic[k])
    time.sleep(timeout)
    ReleaseKey(direct_dic[k])


def find_pso(dm):
    """找怪"""
    ks = "UP"
    time1 = time.time() + 10
    while time1 > time.time():
        XY = Find_use()
        xy = Find_monster()
        print(XY, xy)
        if (XY or xy) is None:
            continue
        try:
            k = ks
            xy = Find_monster()
            XY = Find_use()
            ks = set_XY(xy, XY, k, "X")
            if ks is True:
                ReleaseKey(direct_dic[k])
                print()
                return
        except:
            pass


def motve_to2(xy):
    """移动到指定位置
    first :优先是X 还是Y
    xy: 目标坐标点
    map_NUB:地图编号
    """
    ks = "UP"
    keys = ["UP", "DOWN", "LEFT", "RIGHT"]
    time1 = time.time() + 5
    while time1 > time.time():
        XY = Find_use()
        if (XY or xy) is None:
            continue
        try:
            k = ks
            XY = Find_use()
            ks = set_XY(xy, XY, k, "X")
            if ks == True:
                ReleaseKey(direct_dic[k])
                return
        except:
            print("报错")


def chushou():
    """出售"""
    FLAG = True
    time1 = time.time() + 20
    while time.time() < time1:
        if get_tiaoguo():
            time.sleep(0.5)
            key_press('ESC')
            time.sleep(0.5)
            break

    if get_shangdian():
        if FLAG:
            key_press("CTRL")
            time.sleep(0.5)
            for i in range(10):
                key_press("X", 0.1, 0.1)
        key_press("NUM1")
        key_press('A')
        key_press('SPACE')
        move('LEFT')
        key_press('SPACE')
        move('RIGHT')
        key_press('ESC')
        key_press('ESC')
        key_press("NUM1")
        time.sleep(1)
    else:
        key_press("CTRL")
        key_press("NUM1")
        key_press("CAPELOCK")
        time.sleep(0.2)
        key_press("NUM1")
        key_press('F12')


def chushou2():
    """风暴出售"""
    FLAG = True
    if get_shangdian():
        time.sleep(3)
        if FLAG:
            key_press("CTRL")
            time.sleep(1)
            for i in range(20):
                key_press("X", 0.1, 0.1)
        key_press("NUM1")
        key_press('A')
        key_press('SPACE')
        move('LEFT')
        key_press('SPACE')
        move('RIGHT')
        key_press('ESC')
        key_press("NUM1")
    else:
        key_press("CTRL")
        key_press("NUM1")
        key_press("CAPELOCK")
        time.sleep(0.2)
        key_press("NUM1")
        key_press('F12')


def Fid_jinbi_youcheng():
    """幽城找金币"""

    resp_mxt = FindString(0, 341, 798, 566, "金", [254, 255], 0.98)
    if resp_mxt != -1:
        X = resp_mxt[-2]
        Y = resp_mxt[-1]
        return int(X), int(Y) + 10
    # resp_mxt = find_image_in_region(0, 0, 600, 800, path + "\IMG\金币.bmp", 0.97, 5)
    # if -1 != resp_mxt:
    #     # print('找到金币')
    #     return resp_mxt[1], resp_mxt[2] + 5

    return None


def Fid_jinbi():
    """找金币"""

    resp_mxt = FindString(0, 341, 798, 566, "金", [254, 255], 0.98)
    if resp_mxt != -1:
        X = resp_mxt[-2]
        Y = resp_mxt[-1]
        return int(X), int(Y) + 10
    # resp_mxt = FindString(0, 200, 800, 561, "雾", "b36bff|ff00ff|68d5ed", 0.98)
    # # resp_mxt = FindString(0, 200, 800, 561, "雾", "ff00ff", 0.98)
    # if resp_mxt != -1:
    #     X = resp_mxt[-2]
    #     Y = resp_mxt[-1]
    #     return int(X) + 5, int(Y) + 5

    ss = Find_SS_String(0, 228, 800, 552)
    if -1 != ss:
        print('找到SS')
        return ss

    return None


def Fid_jinbi3():
    """找ss"""
    ss = Find_SS_String(0, 228, 800, 552)
    if -1 != ss:
        print('找到SS')
        return ss
    resp_mxt = FindString(0, 200, 800, 561, "武", "ff00ff", 0.97)
    if resp_mxt != -1:
        X = resp_mxt[-2]
        Y = resp_mxt[-1]
        return int(X) + 5, int(Y) + 5

    return None


def Fid_jinbi2():
    resp_mxt = find_image_in_region(0, 200, 800, 561, path + "\IMG\金币.bmp", 0.99, 5)
    if -1 != resp_mxt:
        # print('找到金币')
        return resp_mxt[1], resp_mxt[2] + 5

    resp_mxt = FindString(0, 200, 800, 561, "间", "ff00ff", 0.98)
    if resp_mxt != -1:
        print("找到时间引导石")
        X = resp_mxt[-2]
        Y = resp_mxt[-1]
        return int(X) + 5, int(Y) + 5

    resp_mxt = FindString(0, 200, 800, 561, "青", "68d5ed", 0.99)
    if resp_mxt != -1:
        print("找到堇菁石")
        X = resp_mxt[-2]
        Y = resp_mxt[-1]
        return int(X) + 5, int(Y) + 5


x_left = 0
x_right = 0
y_up = 0
y_down = 0


def yidong(monster_box, hero_xywh):
    keys = ["UP", "DOWN", "LEFT", "RIGHT"]
    global x_left, x_right, y_up, y_down
    if abs(hero_xywh[0] - monster_box[0]) >= 14:
        if monster_box[0] > hero_xywh[0]:
            # 角色在左
            # print("角色在左")
            if x_left == 1:
                ReleaseKey(direct_dic['LEFT'])  # 弹起
                x_left = 0
            elif x_right == 1:
                pass
            elif x_right == 0:
                if abs(hero_xywh[0] - monster_box[0]) > 80:
                    # PressKey(direct_dic['RIGHT'])
                    # time.sleep(0.07)
                    # ReleaseKey(direct_dic['RIGHT'])  # 弹起
                    # time.sleep(0.02)
                    PressKey(direct_dic['RIGHT'])
                else:
                    PressKey(direct_dic['RIGHT'])
                x_right = 1
            # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        else:
            # 角色在右
            # print("角色在右")
            if x_right == 1:
                ReleaseKey(direct_dic['RIGHT'])  # 弹起
                x_right = 0
            elif x_left == 1:
                pass
            elif x_left == 0:
                if abs(hero_xywh[0] - monster_box[0]) > 80:
                    # PressKey(direct_dic['LEFT'])
                    # time.sleep(0.02)
                    # ReleaseKey(direct_dic['LEFT'])  # 弹起
                    # time.sleep(0.02)
                    PressKey(direct_dic['LEFT'])
                else:
                    PressKey(direct_dic['LEFT'])
                x_left = 1

    if abs(hero_xywh[1] - monster_box[1]) > 5:
        if monster_box[1] < hero_xywh[1]:
            # 角色在下
            # print("角色在下")
            if y_down == 1:
                ReleaseKey(direct_dic['DOWN'])  # 弹起
                y_down = 0
            elif y_up == 1:
                pass
            elif y_down == 0:
                PressKey(direct_dic['UP'])
                y_up = 1
        else:
            # 角色在上
            # print("角色在上")
            if y_up == 1:
                ReleaseKey(direct_dic['UP'])  # 弹起
                y_up = 0
            elif y_down == 1:
                pass
            elif y_down == 0:
                PressKey(direct_dic['DOWN'])
                y_down = 1


def Get_jinbi(shengao=133):
    """拾取金币"""
    global x_left, x_right, y_up, y_down
    ks = None
    time1 = time.time() + 4
    while time1 > time.time():
        xy = Fid_jinbi()
        if xy is not None:
            try:
                XY = Find_use(shengao)
                # ks = set_XY(xy, XY, ks, first)
                yidong(xy, XY)
                # ReleaseKey(direct_dic[ks])
            except Exception as e:
                print(ks)
                print("报错", e)

        else:
            if x_left == 1:
                ReleaseKey(direct_dic['LEFT'])  # 弹起
            elif x_right == 1:
                ReleaseKey(direct_dic['RIGHT'])  # 弹起
            elif y_up == 1:
                ReleaseKey(direct_dic['UP'])  # 弹起
            elif y_down == 1:
                ReleaseKey(direct_dic['DOWN'])  # 弹起
            x_left = 0
            x_right = 0
            y_up = 0
            y_down = 0
            if ks is not None:
                ReleaseKey(direct_dic[ks])
            keys = ["UP", "DOWN", "LEFT", "RIGHT"]
            for I in keys:
                ReleaseKey(direct_dic[I])
            # print('弹起全部按键')
            return
    keys = ["UP", "DOWN", "LEFT", "RIGHT"]
    for I in keys:
        ReleaseKey(direct_dic[I])


def Get_jinbi2(shengao=133):
    """找金币"""
    global x_left, x_right, y_up, y_down
    ks = None
    time1 = time.time() + 4
    while time1 > time.time():
        xy = Fid_jinbi2()
        if xy is not None:
            try:
                XY = Find_use(shengao)
                # ks = set_XY(xy, XY, ks, first)
                yidong(xy, XY)
                # ReleaseKey(direct_dic[ks])
            except Exception as e:
                print(ks)
                print("报错", e)

        else:
            if x_left == 1:
                ReleaseKey(direct_dic['LEFT'])  # 弹起
            elif x_right == 1:
                ReleaseKey(direct_dic['RIGHT'])  # 弹起
            elif y_up == 1:
                ReleaseKey(direct_dic['UP'])  # 弹起
            elif y_down == 1:
                ReleaseKey(direct_dic['DOWN'])  # 弹起
            x_left = 0
            x_right = 0
            y_up = 0
            y_down = 0
            if ks is not None:
                ReleaseKey(direct_dic[ks])
            keys = ["UP", "DOWN", "LEFT", "RIGHT"]
            for I in keys:
                ReleaseKey(direct_dic[I])
            # print('弹起全部按键')
            return
    keys = ["UP", "DOWN", "LEFT", "RIGHT"]
    for I in keys:
        ReleaseKey(direct_dic[I])


def Get_jinbi3(shengao=133):
    """找金币"""
    global x_left, x_right, y_up, y_down
    ks = None
    time1 = time.time() + 4
    while time1 > time.time():
        xy = Fid_jinbi3()
        if xy is not None:
            try:
                XY = Find_use(shengao)
                # ks = set_XY(xy, XY, ks, first)
                yidong(xy, XY)
                # ReleaseKey(direct_dic[ks])
            except Exception as e:
                print(ks)
                print("报错", e)

        else:
            if x_left == 1:
                ReleaseKey(direct_dic['LEFT'])  # 弹起
            elif x_right == 1:
                ReleaseKey(direct_dic['RIGHT'])  # 弹起
            elif y_up == 1:
                ReleaseKey(direct_dic['UP'])  # 弹起
            elif y_down == 1:
                ReleaseKey(direct_dic['DOWN'])  # 弹起
            x_left = 0
            x_right = 0
            y_up = 0
            y_down = 0
            if ks is not None:
                ReleaseKey(direct_dic[ks])
            keys = ["UP", "DOWN", "LEFT", "RIGHT"]
            for I in keys:
                ReleaseKey(direct_dic[I])
            # print('弹起全部按键')
            return
    keys = ["UP", "DOWN", "LEFT", "RIGHT"]
    for I in keys:
        ReleaseKey(direct_dic[I])


def get_caizhizhuanhuan():
    """获取材质转换"""
    caizhi = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\材质转换提示.bmp", 0.9)
    if '-1' not in str(caizhi):
        print("发现<材质转换>")
        key_press('ESC')
        time.sleep(0.2)


def get_changwan():
    """点击畅玩任务领道具"""
    changwan = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\畅玩任务.bmp", 0.95, 5)
    print(changwan)
    if '-1' not in str(changwan):
        print("开始领取畅玩任务")
        X = changwan[1]
        Y = changwan[2]
        click(int(X), int(Y))
        time.sleep(1)
        for i in [(358, 232), (359, 296), (359, 363), (358, 445), (358, 169), (358, 168), (358, 168)]:
            click(i[0], i[1])
            time.sleep(1)
        key_press('ESC')

    else:
        print("畅玩任务未完成")


def jintu(nandu=2):
    """从赛利亚房间进入摇篮冒险"""
    time.sleep(1)
    move('RIGHT', timeout=3)
    changwan = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\飞艇.bmp", 0.89)
    if changwan != -1:
        print("找到飞艇")
        X = changwan[1]
        Y = changwan[2]
        click(int(X), int(Y))
        time.sleep(0.21)
    key_press('SPACE')
    time.sleep(1)
    click(566, 211)  # 控制板
    time.sleep(0.5)
    click(454, 22)  # 毁坏的克洛诺斯诸岛
    time.sleep(0.5)
    click(196, 292)  # 控制板
    time.sleep(0.5)
    key_press('SPACE')
    time.sleep(1)
    move('RIGHT', timeout=3)
    time.sleep(2)
    for i in range(5):
        move('LEFT', timeout=0.1)
        time.sleep(0.2)

    for i in range(1, nandu):
        move('RIGHT', timeout=0.1)
        time.sleep(0.2)
    time.sleep(1)
    key_press('SPACE')
    time.sleep(2)


def jintu_haibolun(nandu=2):
    """从赛利亚房间进入海伯伦"""
    time.sleep(1)
    move('RIGHT', timeout=3)
    changwan = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\飞艇.bmp", 0.89)
    if changwan != -1:
        print("找到飞艇")
        X = changwan[1]
        Y = changwan[2]
        click(int(X), int(Y))
        time.sleep(0.21)
    key_press('SPACE')
    time.sleep(1)
    click(566, 211)  # 控制板
    time.sleep(0.5)
    click(454, 22)  # 毁坏的克洛诺斯诸岛
    time.sleep(0.5)
    click(196, 292)  # 控制板
    time.sleep(0.5)
    key_press('SPACE')
    time.sleep(1)
    move('RIGHT', timeout=3)
    time.sleep(2)
    hbl = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\海伯伦.bmp", 0.98)
    if hbl == -1:
        print("点击海伯伦")
        click(362, 245)
        time.sleep(0.2)

    for i in range(5):
        move('LEFT', timeout=0.1)
        time.sleep(0.2)

    for i in range(1, nandu):
        move('RIGHT', timeout=0.1)
        time.sleep(0.2)
    time.sleep(1)
    key_press('SPACE')
    time.sleep(2)


def jintu_shengdian(nandu):
    """从赛利亚房间进入圣殿普通"""
    time.sleep(1)
    print("点击活动按钮")
    move('RIGHT', timeout=3)
    changwan = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\飞艇.bmp", 0.89)
    if changwan != -1:
        print("找到飞艇")
        X = changwan[1]
        Y = changwan[2]
        click(int(X), int(Y))
        time.sleep(0.21)
    key_press('SPACE')
    time.sleep(1)
    click(566, 211)  # 控制板
    time.sleep(0.5)
    click(454, 22)  # 毁坏的克洛诺斯诸岛
    time.sleep(0.5)
    click(178, 411)  # 圣域边界
    time.sleep(0.5)
    key_press('SPACE')
    time.sleep(1)
    move('LEFT', timeout=10)
    time.sleep(2)
    shengdian = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\圣殿选图特征.bmp", 0.95)
    print('圣殿选图特征', shengdian)
    if shengdian == -1:
        click(331, 247)  # 圣殿的位置
    time.sleep(0.2)
    for i in range(5):
        move('LEFT', timeout=0.1)
        time.sleep(0.2)

    if nandu == 1:
        pass
    else:
        for i in range(1, nandu):
            move('RIGHT', timeout=0.1)
            time.sleep(0.2)
    time.sleep(1)
    key_press('SPACE')
    time.sleep(2)


def jintu_fengbao(nandu=2):
    """从赛利亚房间进入风暴幽城"""
    time.sleep(1)
    move('RIGHT', timeout=3)
    changwan = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\次元风暴.bmp", 0.89)
    if changwan != -1:
        X = changwan[1]
        Y = changwan[2]
        click(int(X), int(Y))
        time.sleep(0.3)
    key_press('SPACE')
    time.sleep(1)
    move('RIGHT', timeout=3)
    time.sleep(2)
    fengbao = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\风暴幽城选图特征.bmp", 0.89)
    print(fengbao)
    if fengbao == -1:
        click(440, 387)  # 风暴幽城的位置
    time.sleep(1)
    for i in range(3):
        move('LEFT', timeout=0.1)
        time.sleep(0.2)
    time.sleep(1)
    key_press('SPACE')
    time.sleep(2)


def jintu_shenyuan(dm, nandu=1):
    """从赛利亚房间进入深渊"""
    time.sleep(1)
    move('RIGHT', timeout=3)
    changwan = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\次元风暴.bmp", 0.89)
    if '-1' not in changwan:
        print("找到飞艇")
        X = changwan.split("|")[1]
        Y = changwan.split("|")[2]
        click(int(X), int(Y))
        time.sleep(0.21)
    key_press('SPACE')
    time.sleep(1)
    move('RIGHT', timeout=3)
    time.sleep(2)
    fengbao = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\均衡仲裁者选图特征.bmp", 0.89)
    print(fengbao)
    if '-1' in fengbao:
        click(384, 356)  # 均衡仲裁者的位置
    time.sleep(1)
    key_press('SPACE')
    time.sleep(2)


def get_zhiye():
    """获取职业"""
    time.sleep(0.2)
    key_press('M')
    time.sleep(0.2)
    res = mk_OCR(188, 235, 297, 273, "a0844b", 0.99)
    time.sleep(0.1)
    key_press('M')
    time.sleep(0.1)
    print(res[:2])
    if res[:2] == '极诣':
        return 148
    elif res[:2] == '聆风':
        return 113
    elif res[:2] == '知源':
        return 112
    elif res[:2] == '光启':
        return 130
    else:
        return 133


def jintu_wudikengdao():
    """从赛利亚房间进入无底坑道"""
    time.sleep(1)
    move('RIGHT', timeout=3)
    changwan = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\飞艇.bmp", 0.98)
    if '-1' not in changwan:
        print("找到飞艇")
        X = changwan[-2]
        Y = changwan[-1]
        click(int(X), int(Y))
        time.sleep(0.21)
    key_press('SPACE')
    time.sleep(1)
    click(566, 211)  # 控制板
    time.sleep(0.5)
    click(335, 19)  # 第一页
    time.sleep(0.5)
    click(240, 364)  # 切斯特小镇-矿山
    time.sleep(0.5)
    key_press('SPACE')
    time.sleep(1)
    move('RIGHT', timeout=3)
    time.sleep(2)
    tzms = FindString(576, 514, 704, 570, "挑战模式", "b99460", 0.99)

    if tzms != -1:
        X = int(tzms[-2])
        Y = int(tzms[-1])
        click(X, Y)
    time.sleep(1)
    kengdao = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\无底坑道.bmp", 0.99)
    print(kengdao)
    if kengdao == -1:
        click(542, 148)  # 无底坑道的位置
    time.sleep(0.5)
    move('LEFT', timeout=0.1)
    time.sleep(1)
    key_press('SPACE')
    time.sleep(2)


def jintu_jingjileyuan():
    """从赛利亚房间进入荆棘乐园"""
    time.sleep(1)
    move('RIGHT', timeout=3)
    changwan = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\飞艇.bmp", 0.98)
    if '-1' not in changwan:
        print("找到飞艇")
        X = changwan[-2]
        Y = changwan[-1]
        click(int(X), int(Y))
        time.sleep(0.21)
    key_press('SPACE')
    time.sleep(1)
    click(566, 211)  # 控制板
    time.sleep(0.5)
    click(335, 19)  # 第一页
    time.sleep(0.5)
    click(401, 238)  # 切斯特小镇-废墟
    time.sleep(0.5)
    key_press('SPACE')
    time.sleep(1)
    move('RIGHT', timeout=3)
    time.sleep(2)
    leyuan = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\荆棘乐园.bmp", 0.99)
    print(leyuan)
    if leyuan == -1:
        click(588, 411)  # 荆棘乐园的位置
    time.sleep(0.5)
    move('RIGHT', timeout=0.1)
    time.sleep(1)
    key_press('SPACE')
    time.sleep(2)


def jintu_fengbaonilin(nandu=3):
    """从赛利亚房间进入风暴逆鳞普通"""
    time.sleep(1)
    move('RIGHT', timeout=3)
    changwan = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\次元风暴.bmp", 0.98)
    if changwan != -1:
        X = changwan[-2]
        Y = changwan[-1]
        click(int(X), int(Y))
        time.sleep(0.21)
        key_press('SPACE')
        time.sleep(1)
        move('RIGHT', timeout=3)
        time.sleep(2)
        fengbao = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\风暴逆鳞普通.bmp", 0.98)
        if fengbao == -1:
            click(538, 214)  # 风暴幽城的位置
        time.sleep(1)
        for i in range(3):
            move('LEFT', timeout=0.1)
            time.sleep(0.2)
        if nandu == 1:
            pass
        else:
            for i in range(1, nandu):
                move('RIGHT', timeout=0.1)
                time.sleep(0.2)
        time.sleep(1)
        key_press('SPACE')
        time.sleep(2)
    else:
        exit()


def get_GBHD():
    """关闭小铃铛"""
    click(1, 1)  # 点击活动按钮
    time.sleep(0.4)
    for i in range(5):
        changwan = find_image_in_region(580, 472, 793, 562, path + r"\IMG\小酱油.bmp", 0.99)
        if changwan != -1:
            print('《活动》展开，准备关闭')
            click(608, 576)  # 点击活动按钮
            time.sleep(0.3)
        else:
            time.sleep(1)
            return


def get_KQHD():
    """开启活动按钮"""
    for i in range(5):
        changwan = find_image_in_region(542, 444, 798, 603, path + r"\IMG\小酱油.bmp", 0.98, 5)
        print(changwan)
        if changwan != -1:
            time.sleep(2)
            print('活动展开了')
            return
        else:
            print('《活动》关闭，准备展开')
            click(608, 576)  # 点击活动按钮
            time.sleep(1)


def Find_men_DK():
    """无底坑道的门"""
    resp_mxt = find_image_in_region(0, 0, 800, 600, path + r"\IMG\{}".format('坑道_门.bmp'), 0.99)
    print(resp_mxt)
    if resp_mxt != -1:
        X = resp_mxt[-2]
        Y = resp_mxt[-1]
        return int(X), int(Y)
    else:
        return None


def back_home():
    """返回城镇，解除虚弱"""
    while True:
        key_press("ESC")
        time.sleep(1)
        res = FindString(373, 426, 628, 565, "返回城镇", "d6c592", 0.99)
        if res != -1:
            X = int(res[-2])
            Y = int(res[-1])
            click(X + 10, Y - 5)
            time.sleep(0.5)
            key_press("SPACE")
            time.sleep(2)
            break
        else:
            continue


def jiechuxuruo():
    """解除虚弱"""
    time.sleep(1)
    click(799, 58)
    time.sleep(1)
    while True:
        time.sleep(1)
        res = FindString(315, 295, 499, 384, "认", "b99460", 0.99)
        print(res)
        if res != -1:
            key_press("ESC")
            time.sleep(0.5)
        get_KQHD()  # 展开活动
        time.sleep(1)
        resp_mxt = find_image_in_region(518, 446, 800, 564, path + r"\IMG\虚弱.bmp", 0.9)
        if resp_mxt != -1:
            print('点击虚弱图标')
            X = resp_mxt[-2]
            Y = resp_mxt[-1]
            click(X, Y)
            time.sleep(0.5)
        get_GBHD()  # 关闭活动
        res2 = FindString(271, 291, 526, 451, "金", "b99460", 0.99)
        if res2 != -1:
            print('点击金币解除')
            X2 = int(res2[-2])
            Y2 = int(res2[-1])
            click(X2 + 15, Y2 + 5)
            time.sleep(1)
        key_press("SPACE")
        time.sleep(2)
        break


def chongxinjintu():
    """重新进图"""
    move('LEFT', timeout=0.3)
    move('RIGHT', timeout=2)
    time.sleep(2)
    tzms = FindString(576, 514, 704, 570, "挑战模式", "b99460", 0.99)
    if tzms != -1:
        X = int(tzms[-2])
        Y = int(tzms[-1])
        click(X, Y)
    time.sleep(1)
    kengdao = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\无底坑道.bmp", 0.98)
    if kengdao == -1:
        click(542, 148)  # 无底坑道的位置
    time.sleep(0.5)
    move('LEFT', timeout=0.1)
    time.sleep(1)
    key_press('SPACE')
    time.sleep(2)


def chongxinjintu_SD():
    """重新进图"""
    move('RIGHT', timeout=0.5)
    move('LEFT', timeout=3)
    time.sleep(2)
    shengdian = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\圣殿选图特征.bmp", 0.95)
    print('圣殿选图特征', shengdian)
    if shengdian == -1:
        click(331, 247)  # 圣殿的位置

    for i in range(5):
        move('LEFT', timeout=0.1)
        time.sleep(0.2)
    time.sleep(1)
    key_press('SPACE')
    time.sleep(3)


if __name__ == '__main__':
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    xpos = 0
    ypos = 0
    width = 800
    length = 600
    INIT_all()
    time.sleep(0.5)
    img1 = '摇篮5图.bmp'

    res = get_shangdian2()
    print(res)
