from libs222.实现移动 import *

import time

direct_dic = {"UP": 0xC8, "DOWN": 0xD0, "LEFT": 0xCB, "RIGHT": 0xCD}

thy = 20
press_delay = 0.1
release_delay = 0.1
atty = 20


def move(direct, material=False, action_cache=None, press_delay=0.1, release_delay=0.1):
    if direct == "RIGHT":
        if action_cache != None:
            if action_cache != "RIGHT":
                if action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[0]])
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[1]])
                else:
                    ReleaseKey(direct_dic[action_cache])
                PressKey(direct_dic["RIGHT"])
                if not material:
                    time.sleep(press_delay)
                    ReleaseKey(direct_dic["RIGHT"])
                    time.sleep(release_delay)
                    PressKey(direct_dic["RIGHT"])
                action_cache = "RIGHT"
                print("向右移动")
            else:
                print("向右移动")
        else:
            PressKey(direct_dic["RIGHT"])
            if not material:
                time.sleep(press_delay)
                ReleaseKey(direct_dic["RIGHT"])
                time.sleep(release_delay)
                PressKey(direct_dic["RIGHT"])
            action_cache = "RIGHT"
            print("向右移动")
        return action_cache

    elif direct == "LEFT":
        if action_cache != None:
            if action_cache != "LEFT":
                if action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[0]])
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[1]])
                else:
                    ReleaseKey(direct_dic[action_cache])
                PressKey(direct_dic["LEFT"])
                if not material:
                    time.sleep(press_delay)
                    ReleaseKey(direct_dic["LEFT"])
                    time.sleep(release_delay)
                    PressKey(direct_dic["LEFT"])
                action_cache = "LEFT"
                print("向左移动")
            else:
                print("向左移动")
        else:
            PressKey(direct_dic["LEFT"])
            if not material:
                time.sleep(press_delay)
                ReleaseKey(direct_dic["LEFT"])
                time.sleep(release_delay)
                PressKey(direct_dic["LEFT"])
            action_cache = "LEFT"
            print("向左移动")
        return action_cache

    elif direct == "UP":
        if action_cache != None:
            if action_cache != "UP":
                if action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[0]])
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[1]])
                else:
                    ReleaseKey(direct_dic[action_cache])
                PressKey(direct_dic["UP"])
                # time.sleep(press_delay)
                # ReleaseKey(direct_dic["UP"])
                # time.sleep(release_delay)
                # PressKey(direct_dic["UP"])
                action_cache = "UP"
                print("向上移动")
            else:
                print("向上移动")
        else:
            PressKey(direct_dic["UP"])
            # time.sleep(press_delay)
            # ReleaseKey(direct_dic["UP"])
            # time.sleep(release_delay)
            # PressKey(direct_dic["UP"])
            action_cache = "UP"
            print("向上移动")
        return action_cache

    elif direct == "DOWN":
        if action_cache != None:
            if action_cache != "DOWN":
                if action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[0]])
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[1]])
                else:
                    ReleaseKey(direct_dic[action_cache])
                PressKey(direct_dic["DOWN"])
                # time.sleep(press_delay)
                # ReleaseKey(direct_dic["DOWN"])
                # time.sleep(release_delay)
                # PressKey(direct_dic["DOWN"])
                action_cache = "DOWN"
                print("向下移动")
            else:
                print("向下移动")
        else:
            PressKey(direct_dic["DOWN"])
            # time.sleep(press_delay)
            # ReleaseKey(direct_dic["DOWN"])
            # time.sleep(release_delay)
            # PressKey(direct_dic["DOWN"])
            action_cache = "DOWN"
            print("向下移动")
        return action_cache

    elif direct == "RIGHT_UP":
        if action_cache != None:
            if action_cache != "RIGHT_UP":
                if action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[0]])
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[1]])
                else:
                    ReleaseKey(direct_dic[action_cache])
                if not material:
                    PressKey(direct_dic["RIGHT"])
                    time.sleep(press_delay)
                    ReleaseKey(direct_dic["RIGHT"])
                    time.sleep(release_delay)
                    PressKey(direct_dic["RIGHT"])
                    time.sleep(press_delay)
                if material:
                    PressKey(direct_dic["RIGHT"])
                PressKey(direct_dic["UP"])
                # time.sleep(release_delay)
                action_cache = "RIGHT_UP"
                print("右上移动")
            else:
                print("右上移动")
        else:
            if not material:
                PressKey(direct_dic["RIGHT"])
                time.sleep(press_delay)
                ReleaseKey(direct_dic["RIGHT"])
                time.sleep(release_delay)
                PressKey(direct_dic["RIGHT"])
                time.sleep(press_delay)
            if material:
                PressKey(direct_dic["RIGHT"])
            PressKey(direct_dic["UP"])
            # time.sleep(press_delay)
            action_cache = "RIGHT_UP"
            print("右上移动")
        return action_cache

    elif direct == "RIGHT_DOWN":
        if action_cache != None:
            if action_cache != "RIGHT_DOWN":
                if action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[0]])
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[1]])
                else:
                    ReleaseKey(direct_dic[action_cache])
                if not material:
                    PressKey(direct_dic["RIGHT"])
                    time.sleep(press_delay)
                    ReleaseKey(direct_dic["RIGHT"])
                    time.sleep(release_delay)
                    PressKey(direct_dic["RIGHT"])
                    time.sleep(press_delay)
                if material:
                    PressKey(direct_dic["RIGHT"])
                PressKey(direct_dic["DOWN"])
                # time.sleep(press_delay)
                action_cache = "RIGHT_DOWN"
                print("右上移动")
            else:
                print("右上移动")
        else:
            if not material:
                PressKey(direct_dic["RIGHT"])
                time.sleep(press_delay)
                ReleaseKey(direct_dic["RIGHT"])
                time.sleep(release_delay)
                PressKey(direct_dic["RIGHT"])
                time.sleep(press_delay)
            if material:
                PressKey(direct_dic["RIGHT"])
            PressKey(direct_dic["DOWN"])
            # time.sleep(press_delay)
            action_cache = "RIGHT_DOWN"
            print("右上移动")
        return action_cache

    elif direct == "LEFT_UP":
        if action_cache != None:
            if action_cache != "LEFT_UP":
                if action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[0]])
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[1]])
                else:
                    ReleaseKey(direct_dic[action_cache])
                if not material:
                    PressKey(direct_dic["LEFT"])
                    time.sleep(press_delay)
                    ReleaseKey(direct_dic["LEFT"])
                    time.sleep(release_delay)
                    PressKey(direct_dic["LEFT"])
                    time.sleep(press_delay)
                if material:
                    PressKey(direct_dic["LEFT"])
                PressKey(direct_dic["UP"])
                # time.sleep(press_delay)
                action_cache = "LEFT_UP"
                print("左上移动")
            else:
                print("左上移动")
        else:
            if not material:
                PressKey(direct_dic["LEFT"])
                time.sleep(press_delay)
                ReleaseKey(direct_dic["LEFT"])
                time.sleep(release_delay)
                PressKey(direct_dic["LEFT"])
                time.sleep(press_delay)
            if material:
                PressKey(direct_dic["LEFT"])
            PressKey(direct_dic["UP"])
            # time.sleep(press_delay)
            action_cache = "LEFT_UP"
            print("左上移动")
        return action_cache

    elif direct == "LEFT_DOWN":
        if action_cache != None:
            if action_cache != "LEFT_DOWN":
                if action_cache not in ["LEFT", "RIGHT", "UP", "DOWN"]:
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[0]])
                    ReleaseKey(direct_dic[action_cache.strip().split("_")[1]])
                else:
                    ReleaseKey(direct_dic[action_cache])
                if not material:
                    PressKey(direct_dic["LEFT"])
                    time.sleep(press_delay)
                    ReleaseKey(direct_dic["LEFT"])
                    time.sleep(release_delay)
                    PressKey(direct_dic["LEFT"])
                    time.sleep(press_delay)
                if material:
                    PressKey(direct_dic["LEFT"])
                PressKey(direct_dic["DOWN"])
                # time.sleep(press_delay)
                action_cache = "LEFT_DOWN"
                print("左下移动")
            else:
                print("左下移动")
        else:
            if not material:
                PressKey(direct_dic["LEFT"])
                time.sleep(press_delay)
                ReleaseKey(direct_dic["LEFT"])
                time.sleep(release_delay)
                PressKey(direct_dic["LEFT"])
                time.sleep(press_delay)
            if material:
                PressKey(direct_dic["LEFT"])
            PressKey(direct_dic["DOWN"])
            # time.sleep(press_delay)
            action_cache = "LEFT_DOWN"
            print("左下移动")
        return action_cache


def move1(k, timeout=0.05):
    """移动方向"""
    PressKey(direct_dic[k])
    time.sleep(timeout)
    ReleaseKey(direct_dic[k])


# def set_XY(monster_box, hero_xywh, first="Y"):
#     global Y_OK
#     action_cache = None
#     if first == "X":
#         if abs(hero_xywh[0] - monster_box[0]) < 20 and abs(hero_xywh[1] - monster_box[1]) < 20:
#             print("在目标附近")
#             return True
#
#         elif monster_box[0] - hero_xywh[0] > 0 and abs(hero_xywh[0] - monster_box[0]) > 20:
#             print("角色在左")
#             # 角色在左
#             move1("RIGHT")
#
#         elif monster_box[0] - hero_xywh[0] < 0 and abs(hero_xywh[0] - monster_box[0]) > 20:
#             print("角色在右")
#             # 角色在右
#             move1("LEFT")
#
#     elif first == 'Y':
#         if monster_box[1] - hero_xywh[1] < 0 and abs(hero_xywh[1] - monster_box[1]) > 10:
#             print("角色在下")
#             # 角色在下
#             move1("UP")
#
#         elif monster_box[1] - hero_xywh[1] > 0 and abs(hero_xywh[1] - monster_box[1]) > 10:
#             print("角色在上")
#             # 角色在上
#             move1("DOWN")
#         else:
#             Y_OK = "OK"
# def set_XY(monster_box, hero_xywh, first="Y"):
#     first = first.upper()
#     if first == "X":
#         if abs(hero_xywh[0] - monster_box[0]) < 20 and abs(hero_xywh[1] - monster_box[1]) < 20:
#             print("在目标附近")
#             return True
#
#         elif abs(hero_xywh[0] - monster_box[0]) > 20:
#             if monster_box[0] > hero_xywh[0]:
#                 print("角色在左")
#                 # 角色在左
#                 move1("RIGHT")
#             else:
#                 print("角色在右")
#                 # 角色在右
#                 move1("LEFT")
#
#         elif abs(hero_xywh[1] - monster_box[1]) > 10:
#             if monster_box[1] < hero_xywh[1]:
#                 print("角色在下")
#                 # 角色在下
#                 move1("UP")
#             else:
#                 print("角色在上")
#                 # 角色在上
#                 move1("DOWN")
#
#     elif first == 'Y':
#         if abs(hero_xywh[1] - monster_box[1]) > 10:
#             if monster_box[1] < hero_xywh[1]:
#                 print("角色在下")
#                 # 角色在下
#                 move1("UP")
#             else:
#                 print("角色在上")
#                 # 角色在上
#                 move1("DOWN")
#
#         elif abs(hero_xywh[0] - monster_box[0]) > 20:
#             if monster_box[0] > hero_xywh[0]:
#                 print("角色在左")
#                 # 角色在左
#                 move1("RIGHT")
#             else:
#                 print("角色在右")
#                 # 角色在右
#                 move1("LEFT")X

def set_XY(monster_box, hero_xywh, k, first="Y"):
    keys = ["UP", "DOWN", "LEFT", "RIGHT"]
    first = first.upper()
    if abs(hero_xywh[0] - monster_box[0]) < 15 and abs(hero_xywh[1] - monster_box[1]) < 12:
        print("在目标附近")
        ReleaseKey(direct_dic[k])
        return k
    if first == "X":
        if abs(hero_xywh[0] - monster_box[0]) > 14:
            if monster_box[0] > hero_xywh[0]:
                # 角色在左
                print("角色在左")
                if k is not None:
                    if k != "RIGHT":
                        ReleaseKey(direct_dic[k])
                        time.sleep(0.02)
                        k = "RIGHT"
                        PressKey(direct_dic[k])
                        time.sleep(0.01)
                        return k
                    else:
                        print("已经按下了", k)
                        k = "RIGHT"
                        return k
                elif k is None:
                    PressKey(direct_dic["LEFT"])
                    return "LEFT"
            else:
                # 角色在右
                print("角色在右")
                if k is not None:
                    if k != "LEFT":
                        ReleaseKey(direct_dic[k])
                        time.sleep(0.02)
                        k = "LEFT"
                        PressKey(direct_dic["LEFT"])
                        return k
                    else:
                        print("已经按下了", k)
                        return k
                elif k is None:
                    PressKey(direct_dic["LEFT"])
                    return "LEFT"


        elif abs(hero_xywh[1] - monster_box[1]) > 12:
            if monster_box[1] < hero_xywh[1]:
                # 角色在下
                print("角色在下")
                if k is not None:
                    if k != "UP":
                        ReleaseKey(direct_dic[k])
                        time.sleep(0.02)
                        k = "UP"
                        PressKey(direct_dic["UP"])
                        return k
                    else:
                        print("已经按下了", k)
                        k = "UP"
                        return k
                elif k is None:
                    PressKey(direct_dic["UP"])
                    return "UP"
            else:
                # 角色在上
                print("角色在上")
                if k is not None:
                    if k != "DOWN":
                        ReleaseKey(direct_dic[k])
                        time.sleep(0.02)
                        k = "DOWN"
                        PressKey(direct_dic["DOWN"])
                        return k
                    else:
                        print("已经按下了 DOWN")
                        k = "DOWN"
                        return k
                elif k is None:
                    PressKey(direct_dic["DOWN"])
                    return "DOWN"

    elif first == 'Y':
        print("YYYYYY")
        if abs(hero_xywh[1] - monster_box[1]) > 12:
            if monster_box[1] < hero_xywh[1]:
                # 角色在下
                print("角色在下")
                if k is not None:
                    if k != "UP":
                        ReleaseKey(direct_dic[k])
                        k = "UP"
                        PressKey(direct_dic["UP"])
                        return k
                    else:
                        print("已经按下了", k)
                        k = "UP"
                        return k

                elif k is None:
                    PressKey(direct_dic["UP"])
                    return "UP"
            else:
                # 角色在上
                print("角色在上")
                if k is not None:
                    if k != "DOWN":
                        ReleaseKey(direct_dic[k])
                        k = "DOWN"
                        PressKey(direct_dic["DOWN"])
                        return k
                    else:
                        print("已经按下了DOWN")
                        k = "DOWN"
                        return k
                elif k is None:
                    PressKey(direct_dic["DOWN"])
                    return "DOWN"

        elif abs(hero_xywh[0] - monster_box[0]) > 14:
            if monster_box[0] > hero_xywh[0]:
                # 角色在左
                print("角色在左")
                if k is not None:
                    if k != "RIGHT":
                        ReleaseKey(direct_dic[k])
                        time.sleep(0.02)
                        k = "RIGHT"
                        PressKey(direct_dic["RIGHT"])
                        return k
                    else:
                        print("已经按下了", k)
                        k = "RIGHT"
                        return k
                elif k is None:
                    PressKey(direct_dic["RIGHT"])
                    return "RIGHT"

            else:
                # 角色在右
                print("角色在右")
                if k is not None:
                    if k != "LEFT":
                        ReleaseKey(direct_dic[k])
                        time.sleep(0.02)
                        k = "LEFT"
                        PressKey(direct_dic["LEFT"])
                        return k
                    else:
                        print("已经按下了", k)
                        k = "LEFT"
                        return k
                elif k is None:
                    PressKey(direct_dic["LEFT"])
                    return "LEFT"


def get_mater(mater_pso, use_foot, first=None):
    """
    mater_pso == G坐标
    use_foot == 角色坐标
    """
    pos = [mater_pso[0] - use_foot[0], mater_pso[1] - use_foot[1]]
    if pos[0] >= 0 and pos[1] <= 0:
        move1('RIGHT', abs(pos[0]) / 440)
        move1('UP', abs(pos[1]) / 420)

    elif pos[0] <= 0 and pos[1] <= 0:
        move1('LEFT', abs(pos[0]) / 440)
        move1('UP', abs(pos[1]) / 420)

    elif pos[0] <= 0 and pos[1] >= 0:
        move1('LEFT', abs(pos[0]) / 440)
        move1('DOWN', abs(pos[1]) / 420)

    elif pos[0] >= 0 and pos[1] >= 0:
        move1('RIGHT', abs(pos[0]) / 440)
        move1('DOWN', abs(pos[1]) / 420)
    return True

def get_mater2(mater_pso, use_foot, first=None):
    """
    mater_pso == G坐标
    use_foot == 角色坐标
    """
    pos = [mater_pso[0] - use_foot[0], mater_pso[1] - use_foot[1]]
    if pos[0] >= 0 and pos[1] <= 0:
        move1('RIGHT', abs(pos[0]) / 340)
        move1('UP', abs(pos[1]) / 200)

    elif pos[0] <= 0 and pos[1] <= 0:
        move1('LEFT', abs(pos[0]) / 340)
        move1('UP', abs(pos[1]) / 200)

    elif pos[0] <= 0 and pos[1] >= 0:
        move1('LEFT', abs(pos[0]) / 340)
        move1('DOWN', abs(pos[1]) / 200)

    elif pos[0] >= 0 and pos[1] >= 0:
        move1('RIGHT', abs(pos[0]) / 340)
        move1('DOWN', abs(pos[1]) / 200)
    return True

def move_to2():
    """

    """


if __name__ == "__main__":
    action_cache = None
    t1 = time.time()
    # while True:
    # if  int(time.time() - t1) % 2 == 0:
    #     action_cache = move("LEFT_DOWN", material=False, action_cache=action_cache, press_delay=0.1, release_delay=0.1)
    # else:
    action_cache = move("RIGHT_UP", material=True, action_cache=action_cache, press_delay=0.1, release_delay=0.1)
