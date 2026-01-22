import ctypes
import sys
import win32gui
from libs222.move_to import get_mater, set_XY
from libs222.点击在游戏生效 import click, direct_dic
from libs222.实现移动 import key_press, PressKey, ReleaseKey
import win32com.client
import os
# import cv2
import mss.tools
# import numpy as np
import time
from win32com.client import Dispatch

path = os.path.dirname(os.path.abspath(sys.argv[0]))
# path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "../"))
xpos = 0
ypos = 0
width = 800
length = 600

sct = mss.mss()


# def find_image_in_region(x1, x2, y1, y2, template, similarity_threshold):
#     """获取屏幕截图"""
#     monitor = {"top": x1, "left": y1, "width": x2, "height": y2}
#     screenshot = sct.grab(monitor)
#     screenshot = np.array(screenshot)
#     screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
#     # 提取感兴趣的区域
#     roi = screenshot[x2: y1, x1:y2]
#     # 转换模板图像和输入图像的数据类型为CV_8U
#     found_locations = template.split("|")
#     for i, template_path in enumerate(found_locations):
#         template = cv2.imdecode(np.fromfile(file=template_path, dtype=np.uint8), cv2.IMREAD_COLOR)
#         template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
#         roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
#         # 进行模板匹配
#         result = cv2.matchTemplate(roi, template, 5)
#         min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
#         # 判断相似度是否超过阈值
#         if max_val >= similarity_threshold:
#             # 计算找到的图像在屏幕上的左上角坐标
#             top_left = i, max_loc[0] + x1, max_loc[1] + x2
#             return top_left
#         else:
#             return -1


def INIT_all():
    """初始化窗口"""
    win32gui.SetForegroundWindow(DNF_CK)
    xpos = 0
    ypos = 0
    width = 800
    length = 600
    win32gui.MoveWindow(DNF_CK, xpos, ypos, width, length, True)


def get_SS(dm):
    for _ in range(2):
        res = dm.Ocr(0, 0, 800, 600, "", "ffb400-000000", 1.0, 0, 0, 0, 0, "", '')
        if res != "":
            print(res)
            print("发现稀有装备")
            key_press("CAPELOCK")
            time.sleep(0.5)
            key_press("SPACE")
            return 1


def get_tiaoguo(dm):
    """找图-翻牌跳过"""
    resp = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\ESC.bmp", '00000000', 0.8, 0, 0)
    if resp[0] == 0:
        print("找到", 'ESC')
        return True


def get_weishiqu(dm):
    """找到SS"""

    resp = dm.FindPic(237, 189, 578, 297, path + r"\IMG\存在ss.bmp", '000000-000000', 0.8, 0, 0)
    if resp[0] == 0:
        time.sleep(3)
        return True


def get_xiuli(dm):
    """找图-翻牌跳过"""
    xiuli = dm.FindStr(343, 248, 640, 454, "确", "ffffff-000000", 1, 0, 2, 0)
    if "-1" in str(xiuli):
        print("没找到 <修理>")
        return False
    else:
        print("找到 <修理>")
        return True


def get_huodong(dm, imgpath):
    """找图-活动图标"""
    resp = dm.FindPic(xpos, ypos, width, length, imgpath, '00000000', 0.9, 0)
    if resp[0] == '0':
        print("找到", imgpath)
        res = resp.split("|")
        return True


def get_PL(dm):
    """读取当前PL值"""
    while True:
        try:
            print('读取PL')
            res = dm.Ocr(697, 582, 753, 602, '', "c8c8c8-000000", 1.0, 0, 0, 0, 0, "", '')
            data = "".join(list(filter(str.isdigit, res))).replace(' ', '')
            print("当前疲劳值为：", (data[:-3]))
            return int(data[:-3])
        except:
            time.sleep(1)
            pass


def get_PL_100(dm):
    """读取不满级角色的当前PL值"""
    while True:
        try:
            print('读取PL')
            res = dm.Ocr(697, 582, 753, 602, '', "c8c8c8-000000", 1.0, 0, 0, 0, 0, "", '')
            data = "".join(list(filter(str.isdigit, res))).replace(' ', '')
            print("当前疲劳值为：", (data[:-3]))
            return int(data[:-3])
        except:
            time.sleep(1)
            return get_PL(dm)


def Find_use(dm, shengao=133):
    """定位角色位置,返回角色当前坐标"""
    resp_mxt = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\基础达标.bmp", "000000", 1.0, 0, 0)
    if resp_mxt[0] == 0:
        print("找到角色")
        X = resp_mxt[-2]
        Y = resp_mxt[-1]
        print('身高', shengao)
        return int(X) + 23, int(Y) + shengao
    return None


def Find_monster(dm):
    """定位角色位置,返回角色当前坐标"""
    resp_mxt = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\怪物.bmp", "000000", 0.8, 4, 0)
    if resp_mxt[0] == 0:
        print("找到怪物")
        X = resp_mxt[-2]
        Y = resp_mxt[-1]
        return int(X) + 10, int(Y) + 30
    else:
        print("没有怪物")
    return None


def Find_5tu(dm, img):
    """定位5图的坐标"""
    resp_mxt = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\{}".format(img), "000000", 0.6, 1, 0)
    if resp_mxt[0] == 0:
        X = resp_mxt[-2]
        Y = resp_mxt[-1]
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


def Find_2tu(dm, img):
    """定位2图的坐标"""
    time.sleep(0.1)
    resp_mxt = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\{}".format(img), "000000", 0.9, 3)

    if resp_mxt[0] == "0":
        X = resp_mxt.split("|")[1]
        Y = resp_mxt.split("|")[2]
        return int(X) - 68, int(Y) + 35
    else:
        return None


def Find_men(dm, img):
    """查找门坐标"""
    resp_mxt = dm.FindPic(440, 190, 808, 596, path + r"\IMG\{} |".format(img) + path + r"\IMG\门1.bmp", "8042ff-000000",
                          0.8, 0,
                          0)
    if resp_mxt[0] != -1:
        X = resp_mxt[-2]
        Y = resp_mxt[-1]
        return int(X), int(Y)
    else:
        return None


def Find_men2(dm, img):
    """查找门坐标"""

    resp_mxt = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\{}".format("摇篮5图.bmp"), "000000", 0.6, 0, 0)
    if resp_mxt[0] == 0:
        X = resp_mxt[-2]
        Y = resp_mxt[-1]
        return int(X) + 60, int(Y) + 138 + 61

    resp_mxt = dm.FindPic(0, 205, 800, 600, path + r"\IMG\门2.bmp", "8042ff-000000",
                          0.8, 0,
                          0)
    if resp_mxt[0] != -1:
        X = resp_mxt[-2]
        Y = resp_mxt[-1]
        return int(X), int(Y)
    else:
        return None


def Find_men_DK(dm, img):
    """查找门坐标"""
    resp_mxt = dm.FindPic(0, 0, 800, 600, path + r"\IMG\{}".format(img), "241ced-000000|201cd6-000000|221ce3-000000",
                          1, 0,
                          0)
    if resp_mxt[0] != -1:
        X = resp_mxt[-2]
        Y = resp_mxt[-1]
        return int(X), int(Y)
    else:
        return None


def Find_exit(dm):
    """打开菜单"""
    guanbi = dm.FindStr(0, 0, 800, 600, "关闭", "50899f-000000", 1, 0, 0, 0)
    if "-1" in str(guanbi):
        print("没找到 <关闭> 菜单打开")
        return False
    else:
        print("找到 <关闭> 菜单关闭")
        return True


def Find_open(dm):
    """判断是否开门"""
    time1 = time.time() + 0.2
    while time1 > time.time():
        resp_mxt = dm.FindPic(650, 25, 799, 139,
                              path + "\IMG\开门信号3.bmp|" + path + r"\IMG\开门信号.bmp|" + path + "\IMG\开门信号2.bmp|" + path + "\IMG\开门信号4.bmp",
                              "000000",
                              0.8, 0, 0)

        if '-1' not in str(resp_mxt):
            return True
    return False


def Find_open_fengbao(dm):
    """判断是否开门"""
    time1 = time.time() + 0.4
    while time1 > time.time():
        resp_mxt = dm.FindPic(603, 19, 806, 148,
                              path + "\IMG\开门信号5.bmp|" + path + r"\IMG\开门信号.bmp|" + path + r"\IMG\开门信号7.bmp|" + path + "\IMG\开门信号2.bmp",
                              "000000",
                              0.75, 0, 0)
        if '-1' not in str(resp_mxt):
            return True
    return False


def Find_open_miwu(dm):
    """判断是否开门"""
    time1 = time.time() + 1
    while time1 > time.time():
        resp_mxt = dm.FindPic(664, 26, 798, 88,
                              path + "\IMG\迷雾开门信号2.bmp|" + path + r"\IMG\迷雾开门信号.bmp|",
                              "000000",
                              0.9, 3)

        if '-1' not in resp_mxt:
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
        resp_mxt = dm.FindPic(664, 26, 798, 88,
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
        resp_mxt = dm.FindPic(664, 26, 798, 88,
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
        resp_mxt = dm.FindPic(664, 26, 798, 88, path + "\IMG\随机深渊.bmp|" + path, "000000", 0.9, 3)

        if '-1' not in resp_mxt:
            print("深渊")
            return True
        else:
            print("没有深渊")
    else:
        return False


def get_user_map(dm):
    """通过地图判断角色在几号房间"""
    print(1)
    boss = dm.FindPic(682, 24, 793, 103, path + r"\IMG\boss房间.bmp", "000000", 0.8, 1)
    if boss[0] == '0':
        print("出现牛头")
        use_map = dm.FindPic(682, 24, 793, 103, path + r"\IMG\地图角色.bmp", "000000", 0.8, 1)
        if use_map[0] == '0':
            print(use_map)
            use_map = use_map.split("|")
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
            boss2 = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\紧急事件后检测.bmp", "000000", 0.9, 1)
            print('boss2 :', boss2)
            if '-1' not in boss2:
                return 6
            jinjishijian = dm.FindPic(682, 24, 793, 103, path + r"\IMG\紧急事件.bmp", "000000", 0.8, 1)
            if jinjishijian[0] == '0':
                print("紧急事件出现")
                return 7
    else:
        print("找不到boss房间")


def get_boos(dm):
    """判断牛头还在不在"""
    boss = dm.FindPic(736, 22, 794, 138, path + r"\IMG\boss房间.bmp", "000000", 0.8, 0, 0)
    if boss[0] == 0:
        return True
    else:
        time.sleep(0.5)
        boss = dm.FindPic(736, 22, 794, 138, path + r"\IMG\boss房间.bmp", "000000", 0.8, 0, 0)
        if boss[0] == -1:
            return False
        else:
            return True


def get_boos_miwu(dm):
    """判断牛头还在不在"""
    boss = dm.FindPic(665, 23, 796, 86, path + r"\IMG\迷雾BOSS校验.bmp", "000000", 0.8, 0, 0)
    if boss[0] == 0:
        return True
    else:
        return False


def get_user_map_YL(dm):
    """通过地图判断角色在几号房间"""

    boss = dm.FindPic(736, 22, 794, 138, path + r"\IMG\boss房间.bmp", "000000", 0.8, 0, 0)
    if boss[0] == 0:
        use_map = dm.FindPic(736, 22, 794, 138, path + r"\IMG\地图角色1.bmp", "000000", 0.7, 0, 0)
        if use_map[0] == 0:
            X = int(use_map[-2])
            Y = int(use_map[-1])
            if X == 765 and Y == 124:
                print("角色在图1")
                return 1
            elif X == 765 and Y == 106:
                print("角色在图2")
                return 2
            elif X == 783 and Y == 106:
                print("角色在图3")
                return 3
            elif X == 783 and Y == 88:
                print("角色在图4")
                return 4
            elif X == 765 and Y == 88:
                print("角色在图5")
                return 5
            elif X == 765 and Y == 70:
                print("角色在图6")
                return 6

        elif use_map[0] == -1:
            boss2 = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\王之摇篮boss.bmp", "000000", 0.8, 0, 0)
            if boss2[0] == 0:
                print("角色在boos房间")
                return 7
            jinjishijian = dm.FindPic(736, 45, 794, 138, path + r"\IMG\紧急事件.bmp", "000000", 0.8, 0, 0)
            if jinjishijian[0] == 0:
                print("紧急事件出现")
                return 8
    else:
        guotu = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\过图.bmp", "000000", 1.0, 0, 0)
        if guotu[0] == 0:
            print("过图中")
            return 0
        else:
            return None


def get_user_map_MWGY(dm):
    """通过地图判断角色在几号房间"""
    boss = dm.FindPic(665, 23, 796, 86, path + r"\IMG\boss房间2.bmp", "000000", 1.0, 0, 0)
    if boss[0] == '0':
        use_map = dm.FindPic(665, 23, 796, 86, path + r"\IMG\地图角色.bmp", "000000", 0.7, 1)
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
            elif X == 764 and Y == 74:
                print("角色在图7")
                return 7

        elif '-1' in use_map:
            jingyingg = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\迷雾精英怪房间.bmp", "000000", 0.9, 1)
            print(jingyingg)
            if jingyingg[0] == '0':
                jingyingg = jingyingg.split("|")
                X = int(jingyingg[1])
                Y = int(jingyingg[2])
                if X == 706 and Y == 67:
                    print("角色在精英怪房间")
                    return 4

    else:
        use_map = dm.FindPic(665, 23, 796, 86, path + r"\IMG\地图角色.bmp", "000000", 0.7, 1)
        print(use_map)
        if use_map[0] == '0':
            use_map = use_map.split("|")
            X = int(use_map[1])
            Y = int(use_map[2])
            if X == 781 and Y == 74:
                print("角色在BOSS房间")
                return 8
        else:
            guotu = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\过图.bmp", "000000", 1, 1)
            if guotu[0] == '0':
                print("过图中")
                return 0
            else:
                return None


def get_user_map_FBYC(dm):
    """风暴通过地图判断角色在几号房间"""
    boss = dm.FindPic(679, 42, 797, 104, path + r"\IMG\boss房间.bmp", "000000", 0.8, 0, 0)
    if boss[0] == 0:
        use_map = dm.FindPic(679, 42, 797, 104, path + r"\IMG\地图角色1.bmp", "000000", 0.8, 0, 0)
        if use_map[0] == 0:
            X = int(use_map[-2])
            Y = int(use_map[-1])
            if X == 693 and Y == 70:
                print("角色在图1")
                return 1
            elif X == 711 and Y == 70:
                print("角色在图2")
                return 2
            elif X == 729 and Y == 70:
                print("角色在图3")
                return 3
            elif X == 747 and Y == 70:
                print("角色在图4")
                return 4
            elif X == 765 and Y == 70:
                print("角色在图5")
                return 5
        elif use_map[0] == -1:
            print("角色在boos房间")
            return 6

        guotu = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\过图.bmp", "000000", 0.8, 0, 0)
        if guotu[0] == 0:
            print("过图中")
            return 0
        else:
            return None


def get_user_map_FBNL(dm):
    """风暴通过地图判断角色在几号房间"""
    boss = dm.FindPic(684, 46, 794, 102, path + r"\IMG\boss房间.bmp", "000000", 0.8, 0, 0)
    if boss[0] == 0:
        use_map = dm.FindPic(684, 46, 794, 102, path + r"\IMG\地图角色1.bmp", "000000", 0.8, 0, 0)
        if use_map[0] == 0:
            X = int(use_map[-2])
            Y = int(use_map[-1])
            if X == 729 and Y == 52:
                print("角色在图1")
                return 1
            elif X == 747 and Y == 52:
                print("角色在图2")
                return 2
            elif X == 765 and Y == 52:
                print("角色在图3")
                return 3
        elif use_map[0] == -1:
            time.sleep(0.2)
            use_map2 = dm.FindPic(684, 46, 794, 102, path + r"\IMG\地图角色1.bmp", "000000", 0.8, 0, 0)
            boss2 = dm.FindPic(684, 46, 794, 102, path + r"\IMG\boss房间.bmp", "000000", 0.8, 0, 0)
            if boss2[0] == 0 and use_map2[0] == -1:
                print("角色在boos房间")
                return 4

        guotu = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\过图.bmp", "000000", 1.0, 0, 0)
        if guotu[0] == 0:
            print("过图中")
            return 0
        else:
            return None


def get_user_map_WDKD(dm):
    """无底坑道通过地图判断角色在几号房间"""
    boss = dm.FindPic(627, 25, 800, 71, path + r"\IMG\boss房间.bmp", "000000", 0.8, 0, 0)
    if boss[0] == 0:
        shenyuuan = dm.FindPic(627, 25, 800, 71, path + r"\IMG\无底坑道深渊.bmp", "000000", 0.8, 0, 0)
        if shenyuuan[0] == 0:
            return 10
        use_map = dm.FindPic(627, 25, 800, 71, path + r"\IMG\地图角色1.bmp", "000000", 0.8, 0, 0)
        if use_map[0] == 0:
            X = int(use_map[-2])
            Y = int(use_map[-1])
            if X == 639 and Y == 52:
                print("角色在图1")
                return 1
            elif X == 657 and Y == 52:
                print("角色在图2")
                return 2
            elif X == 675 and Y == 52:
                print("角色在图3")
                return 3
            elif X == 693 and Y == 52:
                print("角色在图4")
                return 4
            elif X == 711 and Y == 52:
                print("角色在图5")
                return 5
            elif X == 729 and Y == 52:
                print("角色在图6")
                return 6
            elif X == 747 and Y == 52:
                print("角色在图7")
                return 7
            elif X == 765 and Y == 52:
                print("角色在图8")
                return 8

        elif use_map[0] == -1:
            print("角色在boos房间")
            return 9

        guotu = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\过图.bmp", "000000", 1.0, 0, 0)
        if guotu[0] == 0:
            print("过图中")
            return 0
        else:
            return None


def get_user_map_SD(dm):
    """圣殿通过地图判断角色在几号房间"""
    boss = dm.FindPic(681, 41, 798, 66, path + r"\IMG\boss房间.bmp", "000000", 0.8, 1)
    if boss[0] == '0':
        use_map = dm.FindPic(681, 41, 798, 66, path + r"\IMG\地图角色.bmp", "000000", 0.8, 1)
        print(use_map)
        if use_map[0] == '0':
            use_map = use_map.split("|")
            X = int(use_map[1])
            Y = int(use_map[2])
            if X == 691 and Y == 56:
                print("角色在图1")
                return 1
            elif X == 709 and Y == 56:
                print("角色在图2")
                return 2
            elif X == 727 and Y == 56:
                print("角色在图3")
                return 3
            elif X == 745 and Y == 56:
                print("角色在图4")
                return 4
            elif X == 763 and Y == 56:
                print("角色在图5")
                return 5
        elif '-1' in use_map:
            jinjishijian = dm.FindPic(736, 45, 794, 138, path + r"\IMG\紧急事件.bmp", "000000", 0.8, 1)
            if jinjishijian[0] == '0':
                print("紧急事件出现")
                for i in range(3):
                    time.sleep(1)
                    shengdian5 = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\圣殿5图特征.bmp", "000000", 0.8, 1)
                    if '-1' not in shengdian5:
                        print("在图5")
                        return 7
                else:
                    return 6
            else:
                return 6

        guotu = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\过图.bmp", "000000", 1, 1)
        if guotu[0] == '0':
            print("过图中")
            return 0
        else:
            return None



def get_shangdian2(dm):
    """寻找<出售>"""

    shangdian = dm.FindStr(5, 432, 113, 545, "出|售", "6094b9-000000", 1, 0, 0, 0)
    if "-1" in str(shangdian):
        return False
    else:
        print("找到 <出售> ")
        return True


def get_use(dm):
    """进入选择角色"""
    while True:
        key_press("ESC")
        time.sleep(1)
        res = dm.FindStr(271, 444, 617, 568, "择|角", "92c5d6-000000", 1, 0, 0, 0)
        if res[0] != -1:
            X = int(res[-2])
            Y = int(res[-1])
            click(X + 10, Y - 5)
            break
        else:
            continue


def back_home(dm):
    """返回城镇，解除虚弱"""
    while True:
        key_press("ESC")
        time.sleep(1)
        res = dm.FindStr(454, 489, 561, 526, "回|城", "92c5d6-000000", 1, 0, 0, 0)
        if res[0] != -1:
            X = int(res[-2])
            Y = int(res[-1])
            click(X + 10, Y - 5)
            time.sleep(0.5)
            key_press("SPACE")
            time.sleep(2)
            break
        else:
            continue


def jiechuxuruo(dm):
    """解除虚弱"""
    time.sleep(1)
    click(799, 58)
    time.sleep(1)
    while True:
        time.sleep(1)
        res = dm.FindStr(315, 295, 499, 384, "确|认", "6094b9-000000", 1, 0, 0, 0)
        if res[0] != -1:
            key_press("ESC")
            time.sleep(0.5)
            get_KQHD(dm)  # 展开活动
            time.sleep(1)
            resp_mxt = dm.FindPic(518, 446, 800, 564, path + r"\IMG\虚弱.bmp", "000000", 0.8, 0, 0)
            if resp_mxt[0] == 0:
                print("找到金币")
                X = resp_mxt[-2]
                Y = resp_mxt[-1]
                click(X, Y)
                time.sleep(0.5)
            get_GBHD(dm)  # 关闭活动
            res2 = dm.FindStr(271, 291, 526, 451, "金|币", "6094b9-000000", 1, 0, 0, 0)
            if res2[0] != -1:
                X2 = int(res2[-2])
                Y2 = int(res2[-1])
                click(X2 + 15, Y2 + 5)
                time.sleep(1)
            key_press("SPACE")
            time.sleep(2)
            break
        else:
            continue


def chongxinjintu(dm):
    """重新进图"""
    move('RIGHT', timeout=1)
    move('RIGHT', timeout=2)
    time.sleep(2)
    tzms = dm.FindStr(576, 514, 704, 570, "挑战模式", "6094b9-000000", 1, 0, 0, 0)
    if tzms[0] == 0:
        X = int(tzms[-2])
        Y = int(tzms[-1])
        click(X, Y)
    time.sleep(1)
    kengdao = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\无底坑道.bmp", "000000", 0.8, 0, 0)
    print(kengdao)
    if kengdao[0] == -1:
        click(542, 148)  # 无底坑道的位置
    time.sleep(0.5)
    move('LEFT', timeout=0.1)
    time.sleep(1)
    key_press('SPACE')
    time.sleep(2)


def Fenjie_SS(dm):
    """分解SS"""
    print("开始分解SS")
    key_press("ESC")
    if Find_exit(dm):
        key_press("ESC")
    time.sleep(1)
    key_press("0")
    time.sleep(1)
    time1 = time.time() + 10
    fenjie = None
    while time1 > time.time():
        fenjie = dm.FindStr(xpos, ypos, width, length, "装|备", "6094b9-000000", 1, 0, 0, 0)
        if "-1" in str(fenjie):
            print("没找到 <装备分解> ")
            time.sleep(1)
            key_press("0")
            time.sleep(2)
            continue
        else:
            print("找到 <装备分解> ")
            xiuli = dm.FindStr(xpos, ypos, width, length, "修", "6094b9-000000", 1, 0, 0, 0)
            if xiuli[0] == 0:
                X = int(xiuli[-2])
                Y = int(xiuli[-1])
                time.sleep(1)
                click(X, Y)
                time.sleep(1)
                click(X, Y)
                time.sleep(0.3)
                key_press("SPACE")
            time.sleep(1)
            break
    if fenjie[0] != -1:
        X = int(fenjie[-2])
        Y = int(fenjie[-1])
        time.sleep(1)
        click(X, Y)
        time.sleep(1)

    y = 311
    for i in range(2):
        x = 488
        for _ in range(8):
            click(x, y)
            x = x + 28
            time.sleep(0.01)
        y += 28
    click(1, 1)
    time.sleep(1)
    fenjie = dm.FindStr(xpos, ypos, width, length, "分|解", "6094b9-000000", 1, 0, 0, 0)
    if fenjie[0] != -1:
        X = int(fenjie[-2])
        Y = int(fenjie[-1])
        click(X, Y)
        time.sleep(1)
        jiazhi = dm.FindStr(xpos, ypos, width, length, "高|价", "3232ff-000000", 1, 0, 0, 0)
        if fenjie[0] != -1:
            X = int(jiazhi[-2])
            Y = int(jiazhi[-1]) + 23
            click(X, Y)

        queren = dm.FindStr(xpos, ypos, width, length, "确|认", "6094b9-000000", 1, 0, 0, 0)
        if fenjie[0] != -1:
            X = int(queren[-2])
            Y = int(queren[-1])
            click(X, Y)
            time.sleep(5)
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
        XY = Find_use(dm)
        xy = Find_monster(dm)
        print(XY, xy)
        if (XY or xy) is None:
            continue
        try:
            k = ks
            xy = Find_monster(dm)
            XY = Find_use(dm)
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
        XY = Find_use(dm, shengao=133)
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


def chushou(dm):
    """出售"""
    FLAG = True
    time1 = time.time() + 20
    while time.time() < time1:
        if get_tiaoguo(dm):
            time.sleep(0.3)
            key_press('ESC')
            time.sleep(0.2)
            break

    if get_shangdian(dm):
        if FLAG:
            key_press("CTRL")
            time.sleep(1.5)
            for i in range(20):
                key_press("X", 0.05, 0.05)
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


def chushou2(dm):
    """风暴出售"""
    FLAG = True
    if get_shangdian(dm):
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


def Fid_jinbi(dm):
    """找金币"""
    # resp_mxt = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\金币.bmp", "000000", 0.9, 0)
    resp_mxt = dm.FindStr(0, 144, 799, 561, "金|币", "ffffff-000000", 1, 0, 0, 0)
    if resp_mxt[0] == 0:
        print("找到金币")
        X = resp_mxt[-2]
        Y = resp_mxt[-1]
        return int(X) - 8, int(Y) + 8
    resp_mxt = dm.FindStr(0, 0, 800, 600, "雾", "ff00ff-000000|ff6bb3-000000|edd568-000000", 1, 0, 0, 0)
    if resp_mxt[0] != -1:
        print("找到雾核")
        X = resp_mxt[-2]
        Y = resp_mxt[-1]
        # return int(X) + 14, int(Y) + 68
        return int(X) - 8, int(Y) + 8
    # resp_mxt = dm.FindStr(0, 0, 800, 600, "雾|核", "ff00ff-000000|b36bff-000000|68d5ed-000000", 1, 0, 0, 0)
    # if resp_mxt[0] != -1:
    #     print("找到雾核")
    #     X = resp_mxt[-2]
    #     Y = resp_mxt[-1]
    #     # return int(X) + 14, int(Y) + 68
    #     return int(X) - 8, int(Y) + 8

    resp_mxt = dm.FindStr(0, 0, 800, 600, "青", "edd568-000000", 1, 0, 0, 0)
    if resp_mxt[0] != -1:
        print("找到堇青石")
        X = resp_mxt[-2]
        Y = resp_mxt[-1]
        # return int(X) + 14, int(Y) + 68
        return int(X) - 8, int(Y) + 8

    resp_mxt = dm.FindStr(0, 0, 800, 600, "武|士", "ff00ff-000000", 1, 0, 0, 0)
    if resp_mxt[0] == 0:
        print("找到武士")
        X = resp_mxt[-2]
        Y = resp_mxt[-1]
        # return int(X) + 14, int(Y) + 68
        return int(X) + 10, int(Y) + 8

    resp_mxt = dm.FindStr(0, 0, 800, 600, "时|间|引|导|石", "ff00ff-000000", 1, 0, 0, 0)
    if resp_mxt[0] == 0:
        print("时间引导石")
        X = resp_mxt[-2]
        Y = resp_mxt[-1]
        # return int(X) + 14, int(Y) + 68
        return int(X) + 10, int(Y) + 8

    res_SS = dm.Ocr(0, 0, 800, 600, "", "00b4ff-000000", 1.0, 0, 0, 1, 0, "", '')
    if res_SS != '':
        res_SS = res_SS.split("|")
        print(len(res_SS[0]))
        if len(res_SS[0]) == 1:
            res_SS2 = 1
        else:
            res_SS2 = int(len(res_SS[0]) / 2)
        return int(res_SS[res_SS2].split(",")[-2]), int(res_SS[res_SS2].split(",")[-1])

    return None


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

    if abs(hero_xywh[1] - monster_box[1]) > 2:
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


jinbi = None
use = None
shiqu = False


def Get_jinbi(shengao=133):
    """拾取金币"""
    global x_left, x_right, y_up, y_down
    time1 = time.time() + 4
    while time1 > time.time():
        xy = jinbi
        if xy is not None:
            XY = use
            try:
                yidong(xy, XY)
                time.sleep(0.001)
            except Exception as e:
                print(e)

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
            keys = ["UP", "DOWN", "LEFT", "RIGHT"]
            for I in keys:
                ReleaseKey(direct_dic[I])
            print('弹起全部按键')
            return
    keys = ["UP", "DOWN", "LEFT", "RIGHT"]
    for I in keys:
        ReleaseKey(direct_dic[I])


def Get_jinbi2(first='X'):
    """拾取金币"""
    global shiqu, jinbi, use
    ks = None
    shiqu = True
    time1 = time.time() + 4
    while time1 > time.time():

        xy = jinbi
        if xy is not None:
            try:
                XY = use
                ks = set_XY(xy, XY, ks, first)
                # ReleaseKey(direct_dic[ks])
            except Exception as e:
                print(jinbi, use)

        else:
            if ks is not None:
                ReleaseKey(direct_dic[ks])
            keys = ["UP", "DOWN", "LEFT", "RIGHT"]
            for I in keys:
                ReleaseKey(direct_dic[I])
            shiqu = False
            return
    keys = ["UP", "DOWN", "LEFT", "RIGHT"]
    for I in keys:
        ReleaseKey(direct_dic[I])
    shiqu = False


def Get_fenzhuang(dm, first='X'):
    """拾取金币"""
    ks = None
    time1 = time.time() + 4
    while time1 > time.time():
        xy = Fid_jinbi(dm)
        if xy is not None:
            try:
                k = ks
                XY = Find_use(dm)
                ks = set_XY(xy, XY, k, first)
                ReleaseKey(ks)
            except:
                print("报错")
        else:
            keys = ["UP", "DOWN", "LEFT", "RIGHT"]
            for I in keys:
                ReleaseKey(direct_dic[I])
            if ks is not None:
                ReleaseKey(direct_dic[ks])
            return
    keys = ["UP", "DOWN", "LEFT", "RIGHT"]
    for I in keys:
        ReleaseKey(direct_dic[I])


def Fid_jinbi2(dm):
    """找金币"""
    res = dm.FindStr(0, 0, 800, 600, "金|币", "ffffff-000000", 1, 0, 0, 0)
    print(res)
    if "-1" in res:
        print("重新加载字库")
        dm.setDict(0, path + r'\MK字库_2.txt')
        time.sleep(3)


def get_caizhizhuanhuan(dm):
    """获取材质转换"""
    caizhi = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\材质转换提示.bmp", "000000", 0.8, 0, 0)
    if caizhi[0] != -1:
        key_press('ESC')
        time.sleep(0.2)


def get_changwan(dm):
    """点击畅玩任务领道具"""
    changwan = dm.FindPic(539, 484, 739, 595, path + r"\IMG\畅玩任务.bmp", "000000", 0.8, 0, 0)
    if changwan[0] != -1:
        print("开始领取畅玩任务")
        X = changwan[-2]
        Y = changwan[-1]
        click(int(X), int(Y))
        time.sleep(1)
        for i in [(358, 232), (359, 296), (359, 363), (358, 445), (358, 169), (358, 168), (358, 168)]:
            click(i[0], i[1])
            time.sleep(1)
    else:
        print("畅玩任务未完成")


def get_GBHD(dm):
    """关闭小铃铛"""
    for i in range(5):
        changwan = dm.FindPic(580, 472, 793, 562, path + r"\IMG\小酱油.bmp", "000000", 0.8, 0, 0)
        if changwan[0] == 0:
            print('《活动》展开，准备关闭')
            click(608, 576)  # 点击活动按钮
        else:
            time.sleep(2)
            return


def get_KQHD(dm):
    """开启活动按钮"""
    for i in range(5):
        changwan = dm.FindPic(580, 472, 793, 562, path + r"\IMG\小酱油.bmp", "000000", 0.8, 0, 0)
        if changwan[0] == -1:
            print('《活动》关闭，准备展开')
            click(608, 576)  # 点击活动按钮
        else:
            time.sleep(2)
            return


def jintu(dm, nandu=2):
    """从赛利亚房间进入摇篮冒险"""
    time.sleep(1)
    move('RIGHT', timeout=3)
    changwan = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\飞艇.bmp", "000000", 0.8, 0, 0)
    if '-1' not in str(changwan):
        print("找到飞艇")
        X = changwan[-2]
        Y = changwan[-1]
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
    time.sleep(4)


def jintu_shengdian(dm, nandu=1):
    """从赛利亚房间进入圣殿普通"""
    time.sleep(1)
    print("点击活动按钮")
    move('RIGHT', timeout=3)
    changwan = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\飞艇.bmp", "000000", 0.8, 1)
    if '-1' not in changwan:
        print("找到飞艇")
        X = changwan.split("|")[1]
        Y = changwan.split("|")[2]
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
    shengdian = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\圣殿选图特征.bmp", "000000", 0.8, 1)
    print(shengdian)
    if '-1' in shengdian:
        click(331, 247)  # 圣殿的位置

    for i in range(5):
        move('LEFT', timeout=0.1)
        time.sleep(0.2)
    time.sleep(1)
    key_press('SPACE')
    time.sleep(2)


def jintu_fengbao(dm, nandu=2):
    """从赛利亚房间进入风暴幽城"""
    time.sleep(1)
    move('RIGHT', timeout=3)
    changwan = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\次元风暴.bmp", "000000", 0.7, 0, 0)
    if changwan:
        print("找到飞艇")
        X = changwan[-2]
        Y = changwan[-1]
        click(int(X), int(Y))
        time.sleep(0.21)
    key_press('SPACE')
    time.sleep(1)
    move('RIGHT', timeout=3)
    time.sleep(2)
    fengbao = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\风暴幽城选图特征.bmp", "000000", 0.8, 0, 0)
    if fengbao[0] == -1:
        click(440, 387)  # 风暴幽城的位置
    time.sleep(1)
    for i in range(3):
        move('LEFT', timeout=0.1)
        time.sleep(0.2)

    for i in range(1, nandu):
        move('RIGHT', timeout=0.1)
        time.sleep(0.2)
    time.sleep(1)
    key_press('SPACE')
    time.sleep(2)


def jintu_fengbaonilin(dm, nandu=3):
    """从赛利亚房间进入风暴逆鳞普通"""
    time.sleep(1)
    move('RIGHT', timeout=3)
    changwan = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\次元风暴.bmp", "000000", 0.7, 0, 0)
    if changwan[0] == 0:
        print("点击次元风暴")
        X = changwan[-2]
        Y = changwan[-1]
        click(int(X), int(Y))
        time.sleep(0.21)
        key_press('SPACE')
        time.sleep(1)
        move('RIGHT', timeout=3)
        time.sleep(2)
        fengbao = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\风暴逆鳞普通.bmp", "000000", 0.8, 0, 0)
        if fengbao[0] == -1:
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


def get_zhiye(dm):
    """读取职业返回身高"""
    time.sleep(0.2)
    key_press('M')
    time.sleep(0.2)
    res = dm.Ocr(188, 235, 297, 273, '', "4b84a0-000000", 1.0, 0, 0, 0, 0, "", '')
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


def jintu_wudikengdao(dm):
    """从赛利亚房间进入无底坑道"""
    time.sleep(1)
    move('RIGHT', timeout=3)
    changwan = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\飞艇.bmp", "000000", 0.8, 0, 0)
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
    tzms = dm.FindStr(576, 514, 704, 570, "挑战模式", "6094b9-000000", 1, 0, 0, 0)
    if tzms[0] == 0:
        X = int(tzms[-2])
        Y = int(tzms[-1])
        click(X, Y)
    time.sleep(1)
    kengdao = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\无底坑道.bmp", "000000", 0.8, 0, 0)
    print(kengdao)
    if kengdao[0] == -1:
        click(542, 148)  # 无底坑道的位置
    time.sleep(0.5)
    move('LEFT', timeout=0.1)
    time.sleep(1)
    key_press('SPACE')
    time.sleep(2)


def jintu_shenyuan(dm, nandu=1):
    """从赛利亚房间进入深渊"""
    time.sleep(1)
    move('RIGHT', timeout=3)
    changwan = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\次元风暴.bmp", "000000", 0.8, 1)
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
    fengbao = dm.FindPic(xpos, ypos, width, length, path + r"\IMG\均衡仲裁者选图特征.bmp", "000000", 0.8, 1)
    print(fengbao)
    if '-1' in fengbao:
        click(384, 356)  # 均衡仲裁者的位置
    time.sleep(1)
    key_press('SPACE')
    time.sleep(2)


if __name__ == '__main__':
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    xpos = 0
    ypos = 0
    width = 800
    length = 600
    DNF_CK = win32gui.FindWindow("地下城与勇士", "地下城与勇士：创新世纪")
    INIT_all()
    time.sleep(2)

    Get_jinbi(155)

    # while True:
    #     res = get_user_map_FBYC(dm)
    #     print(res)
    #     exit()
    # get_PL(dm)
    # img1 = '摇篮5图.bmp'
    # # while True:
    # #     get_user_map_SD(dm)
    # Fid_jinbi(dm)
    # Get_jinbi(dm)
    # for i in range(5):
    #     t = time.time()
    #     res = Find_5tu(dm, img1)
    #     print(time.time() - t)
    # print(res)
    # while True:
    #     get_weishiqu(dm)
    # while True:
    #     time.sleep(1)
    #     xy = Find_open(dm)
    #     print(xy)
    #     break
    # get_zaicitiaozhan(dm)
    # print(time.time())
    # res1 = Find_use(dm)
    # print(res1)
    # move("LEFT", timeout=0.2)
    # res2 = Find_use(dm)
    # print(res2)
    # v = (res2[0] - res1[0]) / 0.2
    # print(v)
    # print(time.time())
    # Fid_jinbi(dm)
