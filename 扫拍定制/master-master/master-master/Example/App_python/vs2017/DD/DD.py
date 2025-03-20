import sys
import os
import cv2
import mss.tools
import numpy as np
import time
import mss
from PIL import Image

path = os.path.dirname(os.path.abspath(sys.argv[0]))
xpos = 0
ypos = 0
width = 800
length = 600
sct = mss.mss()
txt = path + r'\tools\MK字库_2.txt'
f = open(txt, 'r', encoding='GBK')


def mk_OCR2(x1, y1, x2, y2, colors, thd, ziku=None):
    DIict = {}
    # 获取字点阵
    txt = path + r'\tools\MK字库_1.txt'
    f2 = open(txt, 'r', encoding='GBK')
    text = f2.read()
    if 'x' == ziku:
        txt = path + r'\tools\MK字库_x.txt'
        f3 = open(txt, 'r', encoding='GBK')
        text = f3.read()
    elif '1' == ziku:
        txt = path + r'\tools\dnf字库.txt'
        f4 = open(txt, 'r', encoding='GBK')
        text = f4.read()
    elif 'pl' == ziku:
        txt = path + r'\tools\MK字库_2.txt'
        f2 = open(txt, 'r', encoding='GBK')
        text = f2.read()

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
                if (m % 4):
                    bin_str = bin_str[:-(m % 4)]
                arr = np.array([list(bin_str[i:i + 11].zfill(11)) for i in range(0, len(bin_str), 11)],
                               dtype=np.float32)
                arr = arr.transpose()  # 做成一个数字矩阵

                DIict[words[1]] = arr
        except:
            pass
    f2.seek(0)
    sct = mss.mss()
    img = sct.grab((x1, y1, x2, y2))
    pil_img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")

    # 将 PIL 图像转换为 NumPy 数组
    img_array = np.array(pil_img)

    # 将 OpenCV 图像转换为灰度图像
    gray_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    output_image = np.zeros_like(gray_img)

    # cv2.imshow('13', gray_img)
    # cv2.waitKey(0)

    # target_color = [tuple(int(color[i:i + 2], 16) for i in (4, 2, 0)) for color in colors.split('|')]
    # 创建一个掩膜，查找与目标颜色相同的像素
    # 定义要保留的灰度值（153 和 154）
    target_gray_values = colors
    # 创建一个掩膜，查找与目标灰度值相同的像素
    mask = np.isin(gray_img, target_gray_values)

    output_image[mask] = gray_img[mask]

    # cv2.imshow('13', output_image)
    # cv2.waitKey(0)

    pil_img = Image.fromarray(output_image)
    cv_img = cv2.cvtColor(np.array(pil_img, dtype=np.float32), cv2.COLOR_BGR2RGB)  # PIL 转 OPCV
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    matched_mask = np.zeros_like(cv_img, dtype=bool)
    matching_keys = []  # 存储符合条件的键值
    for k, v in DIict.items():
        vb = v[:5]
        result = cv2.matchTemplate(vb, cv_img, 3)
        locations = np.where(result >= thd)  # 找到满足条件的位置
        if len(locations[0]) > 0:
            row_indices, col_indices = locations
            for row, col in zip(row_indices, col_indices):
                print(k)
                # 检查该区域是否已经匹配过
                # if not np.any(matched_mask[row:row + vb.shape[0], col:col + vb.shape[1]]):
                matching_keys.append(((row, col), k))
                # 标记该区域为已匹配
                # matched_mask[row:row + vb.shape[0], col:col + vb.shape[1]] = True
    sorted_keys = sorted(matching_keys, key=lambda item: item[0][1])  # 按照 x 坐标从左到右排序
    sorted_keys = [k for _, k in sorted_keys]  # 提取键值
    sorted_keys_str = ''.join(sorted_keys)
    return sorted_keys_str


def get_ziku(ziku=None):
    """读取字库，返回字库数组"""
    DIict = {}
    txt = path + r'\tools\MK字库_1.txt'
    f2 = open(txt, 'r', encoding='GBK')
    text = f2.read()

    # 获取字点阵
    if 'x' == ziku:
        txt = path + r'\tools\MK字库_x.txt'
        f2 = open(txt, 'r', encoding='GBK')
        text = f2.read()
    elif '1' == ziku:
        txt = path + r'\tools\dnf字库.txt'
        f2 = open(txt, 'r', encoding='GBK')
        text = f2.read()
    elif 'ceshi' == ziku:
        txt = path + r'\tools\dnf字库ceshi.txt'
        f2 = open(txt, 'r', encoding='GBK')
        text = f2.read()
    elif 'pl' == ziku:
        txt = path + r'\tools\MK字库_2.txt'
        f2 = open(txt, 'r', encoding='GBK')
        text = f2.read()

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
                if (m % 4):
                    bin_str = bin_str[:-(m % 4)]
                arr = np.array([list(bin_str[i:i + 11].zfill(11)) for i in range(0, len(bin_str), 11)],
                               dtype=np.float32)
                arr = arr.transpose()  # 做成一个数字矩阵

                DIict[words[1]] = arr, words[-1]
        except:
            pass
    return DIict


def mk_OCR(x1, y1, x2, y2, colors, thd, ziku=None):
    DIict = get_ziku(ziku)

    sct = mss.mss()
    img = sct.grab((x1, y1, x2, y2))
    pil_img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")

    # 将 PIL 图像转换为 NumPy 数组
    img_array = np.array(pil_img)
    original_img = img_array.copy()
    # 将 OpenCV 图像转换为灰度图像
    gray_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    output_image = np.zeros_like(gray_img)

    # 定义要保留的灰度值
    target_gray_values = colors
    # 创建一个掩膜，查找与目标灰度值相同的像素
    mask = np.isin(gray_img, target_gray_values)

    output_image[mask] = gray_img[mask]

    pil_img = Image.fromarray(output_image)

    cv_img = cv2.cvtColor(np.array(pil_img, dtype=np.float32), cv2.COLOR_BGR2RGB)  # PIL 转 OPCV
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    matched_mask = np.zeros_like(cv_img, dtype=bool)

    matching_keys = []  # 存储符合条件的键值
    for k, v in DIict.items():
        goadu = int([v[-1]][0])
        if goadu > 11:
            goadu = 11
        vb = v[0][:goadu]
        result = cv2.matchTemplate(vb, cv_img, 3)

        locations = np.where(result >= thd)  # 找到满足条件的位置
        if len(locations[0]) > 0:
            row_indices, col_indices = locations
            for row, col in zip(row_indices, col_indices):
                # 提取待匹配区域
                roi = cv_img[row:row + vb.shape[0], col:col + vb.shape[1]]
                # 检查待匹配区域和模板的大小是否一致
                if roi.shape == vb.shape:
                    # 检查像素点是否完全重合
                    if np.all((roi > 0) == (vb > 0)):
                        # 检查该区域是否已经匹配过
                        if not np.any(matched_mask[row:row + vb.shape[0], col:col + vb.shape[1]]):
                            # 检查四个方向是否为空
                            top = row - 1
                            bottom = row + vb.shape[0] + 1
                            left = col - 1
                            right = col + vb.shape[1]

                            # 检查上方是否有非零像素
                            if top >= 0:
                                top_region = cv_img[top, col:col + vb.shape[1]]
                                if np.any(top_region > 0):
                                    continue
                            # # 检查下方是否有非零像素
                            if bottom < cv_img.shape[0]:
                                bottom_region = cv_img[bottom:bottom + 1, col:col + vb.shape[1]]
                                if np.any(bottom_region > 0):
                                    continue
                            # # 检查左方是否有非零像素
                            if left >= 0:
                                left_region = cv_img[row:row + vb.shape[0], left:left + 1]
                                if np.any(left_region > 0):
                                    continue
                            # # 检查右方是否有非零像素
                            if right < cv_img.shape[1]:
                                right_region = cv_img[row:row + vb.shape[0], right:right + 1]
                                if np.any(right_region > 0):
                                    continue

                            matching_keys.append(((row, col), k))
                            # 标记该区域为已匹配
                            matched_mask[row:row + vb.shape[0], col:col + vb.shape[1]] = True

    sorted_keys = sorted(matching_keys, key=lambda item: item[0][1])  # 按照 x 坐标从左到右排序
    sorted_keys = [k for _, k in sorted_keys]  # 提取键值
    sorted_keys_str = ''.join(sorted_keys)
    return sorted_keys_str


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
    # print(list(gray_img))
    #
    # cv2.imshow('huidu', gray_img)
    # cv2.waitKey(0)

    output_image = np.zeros_like(gray_img)
    # 创建一个掩膜，查找与目标颜色相同的像素
    target_gray_values = colors
    # 创建一个掩膜，查找与目标灰度值相同的像素
    mask = np.isin(gray_img, target_gray_values)

    output_image[mask] = gray_img[mask]

    pil_img = Image.fromarray(output_image)
    cv_img = cv2.cvtColor(np.array(pil_img, dtype=np.float32), cv2.COLOR_BGR2RGB)  # PIL 转 OPCV

    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('shaixuan', output_image)
    # cv2.waitKey(0)
    result = cv2.matchTemplate(arr, cv_img, 3)
    minv, maxv, minl, maxl = cv2.minMaxLoc(result)
    if maxv < thd:
        pass
    else:
        return maxl[0] + x1, maxl[1] + y1
    return -1


def find_image_in_region_keke(x1, y1, x2, y2, screenshot2, similarity_threshold, fangshi=3):
    """获取屏幕截图
    :rtype: object
    """
    sct = mss.mss()
    monitor = {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}
    screenshot = sct.grab(monitor)
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.IMREAD_COLOR)
    try:
        template = screenshot2
        roi = cv2.cvtColor(screenshot, cv2.IMREAD_COLOR)
        # 进行模板匹配
        result = cv2.matchTemplate(roi, template, fangshi)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # 判断相似度是否超过阈值
        if max_val >= similarity_threshold:
            # 计算找到的图像在屏幕上的左上角坐标
            top_left = max_loc[0] + x1, max_loc[1] + y1
            return top_left
        else:
            pass
    except Exception as e:
        print(e)
    return -1


def get_screenshot2(x1, y1, x2, y2):
    """获取桌面的第一个图"""
    monitor = {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}
    screenshot = sct.grab(monitor)
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.IMREAD_COLOR)
    return screenshot


def find_image_in_region(x1, y1, x2, y2, template, similarity_threshold, fangshi=3):
    """获取屏幕截图
    :rtype: object
    """
    monitor = {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}
    sct = mss.mss()
    screenshot = sct.grab(monitor)
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.IMREAD_COLOR)
    # 提取感兴趣的区域
    # roi = screenshot[y1:y2, x1:x2]
    #
    # cv2.imshow("image", screenshot)
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


class keke_tools:
    """找图，和文字识别功能"""

    def __init__(self):
        self.pat_list = [
            path + r'\tools\MK字库_1.txt',
            path + r'\tools\MK字库_x.txt',
            path + r'\tools\dnf字库.txt',
            path + r'\tools\MK字库_2.txt'
        ]
        self.all_dict = []
        get_ziku(self)

    def get_ziku(self):
        """读取字库，返回字库数组"""

        for ziku_path in self.pat_list:
            DIict = {}
            f = open(ziku_path, 'r', encoding='GBK')
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
                        if (m % 4):
                            bin_str = bin_str[:-(m % 4)]
                        arr = np.array([list(bin_str[i:i + 11].zfill(11)) for i in range(0, len(bin_str), 11)],
                                       dtype=np.float32)
                        arr = arr.transpose()  # 做成一个数字矩阵

                        DIict[words[1]] = arr, words[-1]
                except:
                    pass
            self.all_dict.append(DIict)

    def mk_OCR(self, x1, y1, x2, y2, colors, thd, ziku=0):
        DIict = self.all_dict[ziku]

        sct = mss.mss()
        img = sct.grab((x1, y1, x2, y2))
        pil_img = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")

        # 将 PIL 图像转换为 NumPy 数组
        img_array = np.array(pil_img)
        original_img = img_array.copy()
        # 将 OpenCV 图像转换为灰度图像
        gray_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        output_image = np.zeros_like(gray_img)

        # 定义要保留的灰度值
        target_gray_values = colors
        # 创建一个掩膜，查找与目标灰度值相同的像素
        mask = np.isin(gray_img, target_gray_values)

        output_image[mask] = gray_img[mask]

        pil_img = Image.fromarray(output_image)

        cv_img = cv2.cvtColor(np.array(pil_img, dtype=np.float32), cv2.COLOR_BGR2RGB)  # PIL 转 OPCV
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        matched_mask = np.zeros_like(cv_img, dtype=bool)

        matching_keys = []  # 存储符合条件的键值
        for k, v in DIict.items():
            goadu = int([v[-1]][0])
            if goadu > 11:
                goadu = 11
            vb = v[0][:goadu]
            result = cv2.matchTemplate(vb, cv_img, 3)

            locations = np.where(result >= thd)  # 找到满足条件的位置
            if len(locations[0]) > 0:
                row_indices, col_indices = locations
                for row, col in zip(row_indices, col_indices):
                    # 提取待匹配区域
                    roi = cv_img[row:row + vb.shape[0], col:col + vb.shape[1]]
                    # 检查待匹配区域和模板的大小是否一致
                    if roi.shape == vb.shape:
                        # 检查像素点是否完全重合
                        if np.all((roi > 0) == (vb > 0)):
                            # 检查该区域是否已经匹配过
                            if not np.any(matched_mask[row:row + vb.shape[0], col:col + vb.shape[1]]):
                                # 检查四个方向是否为空
                                top = row - 1
                                bottom = row + vb.shape[0] + 1
                                left = col - 1
                                right = col + vb.shape[1]

                                # 检查上方是否有非零像素
                                if top >= 0:
                                    top_region = cv_img[top, col:col + vb.shape[1]]
                                    if np.any(top_region > 0):
                                        continue
                                # # 检查下方是否有非零像素
                                if bottom < cv_img.shape[0]:
                                    bottom_region = cv_img[bottom:bottom + 1, col:col + vb.shape[1]]
                                    if np.any(bottom_region > 0):
                                        continue
                                # # 检查左方是否有非零像素
                                if left >= 0:
                                    left_region = cv_img[row:row + vb.shape[0], left:left + 1]
                                    if np.any(left_region > 0):
                                        continue
                                # # 检查右方是否有非零像素
                                if right < cv_img.shape[1]:
                                    right_region = cv_img[row:row + vb.shape[0], right:right + 1]
                                    if np.any(right_region > 0):
                                        continue

                                matching_keys.append(((row, col), k))
                                # 标记该区域为已匹配
                                matched_mask[row:row + vb.shape[0], col:col + vb.shape[1]] = True

        sorted_keys = sorted(matching_keys, key=lambda item: item[0][1])  # 按照 x 坐标从左到右排序
        sorted_keys = [k for _, k in sorted_keys]  # 提取键值
        sorted_keys_str = ''.join(sorted_keys)
        return sorted_keys_str


if __name__ == '__main__':
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    xpos = 0
    ypos = 0
    width = 800
    length = 600
    time.sleep(0.5)
    img1 = '摇篮5图.bmp'
    # tzms = FindString(576, 514, 704, 570, "挑战模式", "b99460", 1)
    # kengdao = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\无底坑道.bmp", 0.9)
    # res = mk_OCR(188, 235, 297, 273, "a0844b", 0.9)
    # res = FindString(271, 291, 526, 451, "金", "b99460", 1)
    # resp_mxt = FindString(0, 0, 800, 600, "青", "68d5ed", 0.99)
    # kengdao = find_image_in_region(xpos, ypos, width, length, path + r"\IMG\无底坑道.bmp", 0.99)

    # tzms = FindString(576, 514, 704, 570, "挑战模式", "b99460", 0.99)
    # print(tzms)
    #     xpos, ypos, width, length = 0, 266, 786, 470
    #     res = Find_men3(xpos, ypos, width, length)
