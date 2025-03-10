import json
import tkinter as tk
from tkinter import filedialog
from ctypes import *
import time
import pyautogui
from huoyandatil import get_xy
import subprocess
from libsall.点击在游戏生效 import click, click2
from libsall.tools import find_image_in_region, Find_exit, mk_OCR  # 找图
import win32gui
import win32con
from libsall.实现移动 import key_press
from tkinter import ttk
from libsall.get_cailiao import get_jiage, huoqujiage, find_24_2_25, Controller, find_shangjia, quxiaoshangjia, \
    shangjia, chazhaobendi
import threading
from pynput import keyboard
import ctypes
import datetime

dd_dll = windll.LoadLibrary(r'tools\dd43390.dll')
dd_dll.DD_btn(0)  # DD Initialize123
import os

if int(time.time()) < 1741598966:
    pass
else:
    exit()
path_entry = None
check_var = None
combo_box1 = None
combo_box2 = None
input_entry = None
jiange_shuru = None
feidengjiashibie = None
guanji_shuru = None
cailiaogeshu_shuru = None
cailiaogeshu_shuru1 = None
jiankongjiage_shuru0 = None
jiankongjiage_shuru1 = None
fankanyeshu_24_shuru = None
fankanyeshu_48_shuru = None
guolvjiage_shuru1 = None
guolvjiage_shuru2 = None
guolvjiage_shuru3 = None
guolvjiage_shuru4 = None
guolvjiage_shuru5 = None
guolvjiage_shuru6 = None
guolvjiage_shuru7 = None
guolvjiage_shuru8 = None
shijian_shuru = None
shichang_shuru = None
cailiao = None
shangjiageshu_shuru = None
jiageshangxian_shuru = None
sousuocishu_shuru = None
sousuoshijian_shuru = None
CONFIG_FILE = "tools\config.json"
yeshu = None


def _set_pwd(pwd):
    # 输入密码
    for i in pwd:
        dd_dll.DD_str(i, 1)


def get_set_pwd(file_path):
    """整理密码本"""
    if file_path:
        try:
            # 读取文件所有行
            with open(file_path, 'r', encoding='utf-8') as fp:
                lines = fp.readlines()

            if lines:
                # 读取第一行
                first_line = lines.pop(0).strip()
                print(f"文件第一行内容为: {first_line}")

                # 要新增的行内容，这里示例为 'New line added'，你可以根据需求修改
                new_line = '\n' + first_line
                lines.append(new_line)

                # 将修改后的内容写回文件
                with open(file_path, 'w', encoding='utf-8') as fp:
                    fp.writelines(lines)

                print("第一行已删除，新行已添加。")
                return first_line
            else:
                print("文件为空，没有可删除的行。")
        except FileNotFoundError:
            print("文件未找到，请检查文件路径。")
        except Exception as e:
            print(f"处理文件时出现错误: {e}")
    else:
        print("请先选择文件")


def select_file():
    # 选择密码路径
    file_path = filedialog.askopenfilename()
    if file_path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, file_path)


def cailiao_file():
    # 选择材料路径
    file_path = filedialog.askopenfilename()
    if file_path:
        cailiao.delete(0, tk.END)
        cailiao.insert(0, file_path)


def login():
    """登录"""
    file_path = path_entry.get()
    first_line = get_set_pwd(file_path)  # 获取密码
    with open('log.log', 'a', encoding='utf-8')as fp:
        first_line = ','.join(first_line)
        now = datetime.datetime.now()
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
        print(formatted_time)
        data = str(formatted_time) + ' ,' + first_line + '\n'
        fp.write(data)
    if first_line:
        result = first_line.split(',')
        qq = result[0]
        pwd = result[1]
        # 查找 WeGame 窗口
        wegame_path = r"WeGame"
        # 使用 subprocess.Popen 启动 WeGame
        subprocess.Popen(wegame_path)
        time.sleep(5)
        print('移动窗口')

        wegame_window = win32gui.FindWindow(None, "WeGame")
        if wegame_window:
            # 将窗口移动到左上角
            win32gui.MoveWindow(wegame_window, 0, 0, 864, 486, True)

            # 激活 WeGame 窗口
            win32gui.SetForegroundWindow(wegame_window)
            time.sleep(1)  # 等待窗口激活
            click2(460, 270)
            click2(460, 270)
            pyautogui.typewrite(qq)  # 输入qq
            pyautogui.press('tab')  # 切换到密码输入框
            time.sleep(0.5)
            _set_pwd(pwd)  # 输入密码
            dd_dll.DD_key(313, 1)
            dd_dll.DD_key(313, 2)  # 回车

            # 过验证码
            time.sleep(8)
            for i in range(3):
                yanzhegnma = find_image_in_region(464, 5, 1013, 527, 'img/验证码.bmp', 0.98)
                print(yanzhegnma)
                if yanzhegnma != -1:
                    print('发现验证码')
                    try:
                        zuobiao = get_xy()  # x y 宽 长
                        for xy in zuobiao:
                            click(xy[0], xy[1])
                            time.sleep(1)
                        click(543, 161)
                        time.sleep(10)
                    except:
                        break
                else:
                    print('无验证码')
                    break

            # 查找 WeGame 窗口
            wegame_window = win32gui.FindWindow(None, "WeGame")
            if wegame_window:
                # 将窗口最大化
                win32gui.ShowWindow(wegame_window, win32con.SW_MAXIMIZE)
                time.sleep(2)
                resp_mxt = find_image_in_region(237, 5, 1299, 361, 'img/dnf图标.bmp', 0.98)
                print(resp_mxt)
                if resp_mxt != -1:
                    X = resp_mxt[1]
                    Y = resp_mxt[2] + 20
                    click2(X, Y)
                    time.sleep(2)
                    dnf_tubiao = find_image_in_region(0, 0, 312, 460, 'img/dnf图标2.bmp', 0.98)
                    if dnf_tubiao != -1:
                        click2(dnf_tubiao[1], dnf_tubiao[2])
                        time.sleep(1)
                    click2(1781, 1002)
                    time.sleep(30)
                else:
                    print("没有dnf图标")
                return None

            else:
                print("未找到 WeGame 窗口。")


def get_windo():
    """窗口移动到左上角"""
    global CK
    try:
        # 查找地下城与勇士窗口
        CK = win32gui.FindWindow("地下城与勇士", "地下城与勇士：创新世纪")
        if CK == 0:
            print("未找到游戏窗口，请检查游戏是否启动。")
            return False

        # 获取窗口的矩形区域，返回值是一个包含 (left, top, right, bottom) 的元组
        left, top, right, bottom = win32gui.GetWindowRect(CK)
        width = right - left
        length = bottom - top

        # 窗口移动到左上角
        xpos = 0
        ypos = 0
        win32gui.MoveWindow(CK, xpos, ypos, width, length, True)

        # 激活游戏窗口
        win32gui.SetForegroundWindow(CK)
        time.sleep(1)

        print("游戏窗口置顶")
        return True
    except Exception as e:
        print("游戏未启动或出现其他错误:", e)
        return False


def get_user():
    # 选择角色
    for i in range(120):
        if get_windo():
            for i in range(120):
                get_use = find_image_in_region(0, 1, 1920, 1080, 'img/选择角色特征.bmp', 0.98)
                print(get_use)
                if get_use != -1:
                    time.sleep(5)
                    key_press("SPACE")
                    time.sleep(5)
                    return True
                else:
                    time.sleep(5)
        else:
            time.sleep(5)
    return False


def get_guanbi():
    """查找关闭图片"""
    time.sleep(3)
    guanbi = find_image_in_region(0, 0, 800, 600, 'img/关闭.bmp', 0.98)
    if guanbi != -1:
        print('找到关闭')
        time.sleep(1)
        click2(guanbi[1], guanbi[2])
        time.sleep(1)


def set_up_seting():
    """初始化设置"""
    get_guanbi()
    click2(171, 421)
    key_press("SPACE")
    key_press("SPACE")
    key_press("SPACE")

    for i in range(3):
        key_press("ESC")
        time.sleep(0.5)
        if find_image_in_region(0, 1, 800, 600, 'img/菜单特征.bmp', 0.98) != -1:
            key_press("ESC")
            time.sleep(0.5)
            break
    key_press("o")
    get_fenbianlv = find_image_in_region(0, 1, 1920, 1080, 'img/4比3.bmp|img/4比3_2.bmp', 0.98)
    if get_fenbianlv != -1:
        print('找到4比3')
        time.sleep(1)
        click2(get_fenbianlv[1] + 77, get_fenbianlv[2])
        time.sleep(0.5)
        click2(get_fenbianlv[1], get_fenbianlv[2])
        baocun = find_image_in_region(0, 1, 1920, 1080, 'img/保存.bmp', 0.98)
        if baocun != -1:
            print('找到保存')
            time.sleep(1)
            click2(baocun[1], baocun[2])
            key_press("SPACE")
            time.sleep(3)
            get_windo()
    else:
        pass


def stop_all():
    """退出wegame 和 dnf"""
    os.system('taskkill /F /IM wegame.exe')
    time.sleep(2)
    os.system('taskkill /F /IM DNF.exe')
    time.sleep(3)


# 定义复选框被点击时的处理函数
def on_checkbox_click():
    if check_var.get() == 1:
        print("复选框被选中")
        stop_all()
        login()
    else:
        check_var.set(1)
        print("复选框被取消选中")


def initsaopai():
    while True:
        key_press("B")
        time.sleep(0.1)
        moren = find_image_in_region(571, 0, 798, 132, "img\默认.bmp", 0.99, 5)
        if moren != -1:
            print("拍卖行打开")
            time.sleep(0.5)
            click2(moren[1] + 10, moren[2] + 5)
            time.sleep(1)
            return

        key_press("ESC")
        time.sleep(0.5)


def time_consuming_task():
    global yeshu
    sousuocishu1 = sousuocishu_shuru.get()
    sousuoshijian1 = sousuoshijian_shuru.get()
    start_button.config(text="暂停/Home")
    while True:
        # 扫拍
        on_checkbox_click()  # 当前角色下线
        get_user()
        get_windo()
        set_up_seting()
        stop_time = int(time.time()) + (int(sousuoshijian1) * 24 * 60 * 60)
        for _ in range(int(sousuocishu1)):
            if stop_time < int(time.time()):
                break
            initsaopai()
            print('初始化完成')

            time.sleep(1)
            name = combo_box1.get()  # 获取物品名称
            fanye24 = fankanyeshu_24_shuru.get()  # 24小时翻页
            fanye48 = fankanyeshu_48_shuru.get()  # 48小时翻页
            geshu = cailiaogeshu_shuru.get()  # 材料个数上限
            geshu1 = cailiaogeshu_shuru1.get()  # 材料个数上限
            zuidi = jiankongjiage_shuru0.get()  # 最低价格
            zuigao = jiankongjiage_shuru1.get()  # 最高价格
            cailiao_dizhi = cailiao.get()  # 材料保存路径
            jiangeshijian = jiange_shuru.get()

            guolv = [guolvjiage_shuru1.get(),
                     guolvjiage_shuru2.get(),
                     guolvjiage_shuru3.get(),
                     guolvjiage_shuru4.get(),
                     guolvjiage_shuru5.get(),
                     guolvjiage_shuru6.get(),
                     guolvjiage_shuru7.get(),
                     guolvjiage_shuru8.get()
                     ]
            guolv_list = [i for i in guolv if i != 0]
            if name in ["设计图", "消耗品", '材料', "‘投掷/设置", "袖珍罐", "其他"]:
                # try:
                moren = find_image_in_region(571, 0, 798, 132, "img\默认.bmp", 0.98)
                if moren != -1:
                    print("拍卖行打开")
                    click2(moren[1], moren[2])
                    time.sleep(1)
                yeshu = get_jiage(name, fanye24, fanye48, geshu, geshu1, zuidi, zuigao, guolv_list, yeshu,
                                  cailiao_dizhi)
            time.sleep(int(jiangeshijian))
    # except Exception as e:
    #     print(e)


def time_consuming_shangjia():
    on_checkbox_click()  # 当前角色下线
    login()
    get_user()
    get_windo()
    set_up_seting()
    cailiao_dizhi = cailiao.get()  # 材料保存路径
    while True:
        # 上架
        if os.path.getsize(cailiao_dizhi) == 0:
            time.sleep(5)
            print('没有东西')
            continue
        else:
            # 读取文件内容
            with open(cailiao_dizhi, 'r', encoding='utf-8') as fp:
                data = fp.readline()
                data_list = data.strip().split(',')
                print(data_list)

            # 清空文件内容
            with open(cailiao_dizhi, 'w', encoding='utf-8') as fp:
                pass
            print("文件内容已清空。")
        name = data_list[0]
        print(name)
        geshu = data_list[1]
        mingwang = data_list[2]
        jiage = data_list[3]
        shijian = data_list[4]
        danjia = jiageshangxian_shuru.get()
        key_press('ESC')
        initsaopai()

        # 根据名字搜到这个图片
        click2(55, 89)
        keyboard = Controller()
        keyboard.type(name)
        time.sleep(0.5)
        click2(658, 89)  # 点击搜索
        time.sleep(2)
        leiming = combo_box1.get()  # 物品分类

        data_xy = find_shangjia(name, geshu, danjia, leiming)
        # 开始上架
        shangjia(data_xy[1], leiming, geshu, jiage, shijian)

    # 打开已经上架的材料，看看有没有重复，有就下架 收邮件
    # 查看背包里面这个材料有没有，数量是多少
    # 如果不够就去一键购买收邮件
    # 再找到这个物品，上架
    # 上架后观察有没有超过20个如果超过了就回到第二页然后只留下10个 收邮件

    pass


def save_config():
    config = {
        "path": path_entry.get(),
        "check_box": check_var.get(),
        "combo_box1": combo_box1.get(),
        "combo_box2": combo_box2.get(),
        "input_entry": input_entry.get(),
        "jiange_shuru": jiange_shuru.get(),
        "feidengjiashibie": feidengjiashibie.get(),
        "guanji_shuru": guanji_shuru.get(),
        "cailiaogeshu_shuru": cailiaogeshu_shuru.get(),
        "cailiaogeshu_shuru1": cailiaogeshu_shuru1.get(),
        "jiankongjiage_shuru0": jiankongjiage_shuru0.get(),
        "jiankongjiage_shuru1": jiankongjiage_shuru1.get(),
        "fankanyeshu_24_shuru": fankanyeshu_24_shuru.get(),
        "fankanyeshu_48_shuru": fankanyeshu_48_shuru.get(),
        "guolvjiage_shuru1": guolvjiage_shuru1.get(),
        "guolvjiage_shuru2": guolvjiage_shuru2.get(),
        "guolvjiage_shuru3": guolvjiage_shuru3.get(),
        "guolvjiage_shuru4": guolvjiage_shuru4.get(),
        "guolvjiage_shuru5": guolvjiage_shuru5.get(),
        "guolvjiage_shuru6": guolvjiage_shuru6.get(),
        "guolvjiage_shuru7": guolvjiage_shuru7.get(),
        "guolvjiage_shuru8": guolvjiage_shuru8.get(),
        "shijian_shuru": shijian_shuru.get(),
        "shichang_shuru": shichang_shuru.get(),
        "cailiao": cailiao.get(),
        "shangjiageshu_shuru": shangjiageshu_shuru.get(),
        "jiageshangxian_shuru": jiageshangxian_shuru.get(),
        "sousuocishu_shuru": sousuocishu_shuru.get(),
        "sousuoshijian_shuru": sousuoshijian_shuru.get(),

    }
    try:
        # 确保保存配置文件的目录存在
        directory = os.path.dirname(CONFIG_FILE)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f)
    except Exception as e:
        print(f"保存配置文件时出错: {e}")


def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        path_entry.delete(0, tk.END)
        path_entry.insert(0, config.get("path", ""))
        check_var.set(config.get("check_box", 0))
        combo_box1.set(config.get("combo_box1", '物品名称'))
        combo_box2.set(config.get("combo_box2", '稀有度'))
        input_entry.delete(0, tk.END)
        input_entry.insert(0, config.get("input_entry", "0"))
        jiange_shuru.delete(0, tk.END)
        jiange_shuru.insert(0, config.get("jiange_shuru", "20"))
        feidengjiashibie.set(config.get("feidengjiashibie", 0))
        guanji_shuru.delete(0, tk.END)
        guanji_shuru.insert(0, config.get("guanji_shuru", "0"))
        cailiaogeshu_shuru.delete(0, tk.END)
        cailiaogeshu_shuru.insert(0, config.get("cailiaogeshu_shuru", "1"))
        cailiaogeshu_shuru1.delete(0, tk.END)
        cailiaogeshu_shuru1.insert(0, config.get("cailiaogeshu_shuru1", "3000"))
        jiankongjiage_shuru0.delete(0, tk.END)
        jiankongjiage_shuru0.insert(0, config.get("jiankongjiage_shuru0", "50000000"))
        jiankongjiage_shuru1.delete(0, tk.END)
        jiankongjiage_shuru1.insert(0, config.get("jiankongjiage_shuru1", "200000000"))
        fankanyeshu_24_shuru.delete(0, tk.END)
        fankanyeshu_24_shuru.insert(0, config.get("fankanyeshu_24_shuru", "3"))
        fankanyeshu_48_shuru.delete(0, tk.END)
        fankanyeshu_48_shuru.insert(0, config.get("fankanyeshu_48_shuru", "3"))
        guolvjiage_shuru1.delete(0, tk.END)
        guolvjiage_shuru1.insert(0, config.get("guolvjiage_shuru1", "0"))
        guolvjiage_shuru2.delete(0, tk.END)
        guolvjiage_shuru2.insert(0, config.get("guolvjiage_shuru2", "0"))
        guolvjiage_shuru3.delete(0, tk.END)
        guolvjiage_shuru3.insert(0, config.get("guolvjiage_shuru3", "0"))
        guolvjiage_shuru4.delete(0, tk.END)
        guolvjiage_shuru4.insert(0, config.get("guolvjiage_shuru4", "0"))
        guolvjiage_shuru5.delete(0, tk.END)
        guolvjiage_shuru5.insert(0, config.get("guolvjiage_shuru5", "0"))
        guolvjiage_shuru6.delete(0, tk.END)
        guolvjiage_shuru6.insert(0, config.get("guolvjiage_shuru6", "0"))
        guolvjiage_shuru7.delete(0, tk.END)
        guolvjiage_shuru7.insert(0, config.get("guolvjiage_shuru7", "0"))
        guolvjiage_shuru8.delete(0, tk.END)
        guolvjiage_shuru8.insert(0, config.get("guolvjiage_shuru8", "0"))
        shijian_shuru.delete(0, tk.END)
        shijian_shuru.insert(0, config.get("shijian_shuru", "0"))
        shichang_shuru.delete(0, tk.END)
        shichang_shuru.insert(0, config.get("shichang_shuru", "0"))
        cailiao.delete(0, tk.END)
        cailiao.insert(0, config.get("cailiao", ""))
        shangjiageshu_shuru.delete(0, tk.END)
        shangjiageshu_shuru.insert(0, config.get("shangjiageshu_shuru", "25"))
        jiageshangxian_shuru.delete(0, tk.END)
        jiageshangxian_shuru.insert(0, config.get("jiageshangxian_shuru", "1000"))

        sousuocishu_shuru.delete(0, tk.END)
        sousuocishu_shuru.insert(0, config.get("sousuocishu_shuru", "300"))
        sousuoshijian_shuru.delete(0, tk.END)
        sousuoshijian_shuru.insert(0, config.get("sousuoshijian_shuru", "3"))


    except FileNotFoundError:
        print("未找到配置文件，使用默认值。")
    except Exception as e:
        print(f"加载配置文件时出错: {e}")


def start_process():
    global task_thread
    # 扫描
    # 创建线程
    task_thread = threading.Thread(target=time_consuming_task)
    # 启动线程
    task_thread.start()
    start_button.config(bg="#00FF00")
    save_config()


def start_shangjia():
    # 上架
    task_thread = threading.Thread(target=time_consuming_shangjia)
    # 启动线程
    task_thread.start()
    shangjia_button.config(bg="#00FF00")
    save_config()


def stop():
    """停止"""
    ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(task_thread.ident), ctypes.py_object(SystemExit))
    start_button.config(text="开始搜索", bg="#808080")


def on_press(key):
    try:
        if key == keyboard.Key.home:
            stop()
    except AttributeError:
        pass


if __name__ == '__main__':
    CK = None
    # 创建主窗口
    root = tk.Tk()
    root.title("扫拍")
    root.geometry("788x570+1132+0")

    # 第一排############################################################
    # 创建输入框用于显示文件路径，设置宽度为 300 像素
    path_entry = tk.Entry(root)
    path_entry.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
    root.columnconfigure(0, minsize=300)

    # 创建选择文件按钮
    select_button = tk.Button(root, text="选择密码本", command=select_file)
    select_button.grid(row=0, column=2, padx=5, pady=5)

    # 定义复选框的变量
    check_var = tk.IntVar()
    checkbox = tk.Checkbutton(root, text="当前账号下线", variable=check_var)
    checkbox.grid(row=0, column=3, padx=5, pady=5)

    # 创建开始按钮，设置大小为 60x60 像素
    start_button = tk.Button(root, text="开始搜索", command=start_process, bg="#808080", relief=tk.RAISED, borderwidth=3,
                             font=("宋体", 15))
    start_button.grid(row=0, column=4, rowspan=5, columnspan=2, padx=5, pady=5, sticky="nsew")
    root.columnconfigure(4, minsize=60)
    root.columnconfigure(5, minsize=60)
    root.rowconfigure(0, minsize=30)
    root.rowconfigure(1, minsize=30)

    # 第二排############################################################
    # 第二排新增 2 个下拉框、一个标签和一个输入框
    combo_box1 = ttk.Combobox(root,
                              values=["武器", "防具", "首饰", "特殊装备", "设计图", "消耗品", '材料',
                                      "‘投掷/设置", "袖珍罐",
                                      "其他", '宠物', '炼金术师', '控偶师', '附魔师', '副职业材料', '辟邪玉', '卡片', '宝珠'],
                              state='readonly')
    combo_box1.set('物品名称')  # 设置默认显示内容
    combo_box1.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    root.columnconfigure(0, minsize=100)

    # 第二个下拉框
    combo_box2 = ttk.Combobox(root, values=["全部", "普通", "高级", "稀有", "神器", "传说", "史诗", "太初"], state='readonly')
    combo_box2.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    combo_box2.set('稀有度')  # 设置默认显示内容
    root.columnconfigure(1, minsize=100)

    # 标签
    mingwang = tk.Label(root, text="名望:")
    mingwang.grid(row=1, column=2, padx=5, pady=5)

    # 输入框
    input_entry = tk.Entry(root, width=20)
    input_entry.grid(row=1, column=3, padx=5, pady=5)
    input_entry.insert(0, "0")  # 在输入框索引 0 的位置插入 "0"

    # 第三排############################################################
    # 间隔时间
    jiange = tk.Label(root, text="间隔时间:")
    jiange.grid(row=2, column=0, padx=5, pady=5)
    # 间隔时间输入框
    jiange_shuru = tk.Entry(root, width=20)
    jiange_shuru.grid(row=2, column=1, padx=5, pady=5)
    jiange_shuru.insert(0, "20")  # 在输入框索引 0 的位置插入 "20"

    # 定义复选框的变量
    feidengjiashibie = tk.IntVar()
    checkbox2 = tk.Checkbutton(root, text="是否识别非等价", variable=feidengjiashibie)
    checkbox2.grid(row=2, column=3, padx=5, pady=5)

    # 第四排############################################################
    # 定时关机
    guanji = tk.Label(root, text="定时关机:")
    guanji.grid(row=3, column=0, padx=5, pady=5)
    # 间隔时间输入框
    guanji_shuru = tk.Entry(root, width=20)
    guanji_shuru.grid(row=3, column=1, padx=5, pady=5)
    guanji_shuru.insert(0, "0")  # 在输入框索引 0 的位置插入 "0"

    # 第五排############################################################
    # 监控价格范围
    jiankongjiage = tk.Label(root, text="监控价格区间:")
    jiankongjiage.grid(row=4, column=0, padx=5, pady=5)
    # 间隔时间输入框
    jiankongjiage_shuru0 = tk.Entry(root, width=20)
    jiankongjiage_shuru0.grid(row=4, column=1, padx=5, pady=5)
    jiankongjiage_shuru0.insert(0, "50000000")  # 在输入框索引 0 的位置插入 "50000000"

    jiankongjiage_shuru1 = tk.Entry(root, width=20)
    jiankongjiage_shuru1.grid(row=4, column=2, padx=5, pady=5)
    jiankongjiage_shuru1.insert(0, "200000000")  # 在输入框索引 0 的位置插入 "200000000"

    # 第六排############################################################
    # 每次翻看页数
    fankanyeshu_24 = tk.Label(root, text="24小时翻看页数:")
    fankanyeshu_24.grid(row=5, column=0, padx=5, pady=5)
    # 间隔时间输入框
    fankanyeshu_24_shuru = tk.Entry(root, width=20)
    fankanyeshu_24_shuru.grid(row=5, column=1, padx=5, pady=5)
    fankanyeshu_24_shuru.insert(0, "3")  # 在输入框索引 0 的位置插入 "3"

    # 每次翻看页数
    fankanyeshu_48 = tk.Label(root, text="48小时翻看页数:")
    fankanyeshu_48.grid(row=5, column=2, padx=5, pady=5)
    # 间隔时间输入框
    fankanyeshu_48_shuru = tk.Entry(root, width=20)
    fankanyeshu_48_shuru.grid(row=5, column=3, padx=5, pady=5)
    fankanyeshu_48_shuru.insert(0, "3")  # 在输入框索引 0 的位置插入 "3"

    # 第七排############################################################
    # 要过滤价格
    guolvjiage = tk.Label(root, text="过滤价格:")
    guolvjiage.grid(row=6, column=0, padx=5, pady=5)
    # 间隔时间输入框
    guolvjiage_shuru1 = tk.Entry(root, width=20)
    guolvjiage_shuru1.grid(row=6, column=1, padx=5, pady=5)
    guolvjiage_shuru1.insert(0, "0")  # 在输入框索引 0 的位置插入 "0"

    guolvjiage_shuru2 = tk.Entry(root, width=20)
    guolvjiage_shuru2.grid(row=6, column=2, padx=5, pady=5)
    guolvjiage_shuru2.insert(0, "0")  # 在输入框索引 0 的位置插入 "0"

    guolvjiage_shuru3 = tk.Entry(root, width=20)
    guolvjiage_shuru3.grid(row=6, column=3, padx=5, pady=5)
    guolvjiage_shuru3.insert(0, "0")  # 在输入框索引 0 的位置插入 "0"

    guolvjiage_shuru4 = tk.Entry(root, width=20)
    guolvjiage_shuru4.grid(row=6, column=4, padx=5, pady=5)
    guolvjiage_shuru4.insert(0, "0")  # 在输入框索引 0 的位置插入 "0"

    guolvjiage_shuru5 = tk.Entry(root, width=20)
    guolvjiage_shuru5.grid(row=7, column=1, padx=5, pady=5)
    guolvjiage_shuru5.insert(0, "0")  # 在输入框索引 0 的位置插入 "0"

    guolvjiage_shuru6 = tk.Entry(root, width=20)
    guolvjiage_shuru6.grid(row=7, column=2, padx=5, pady=5)
    guolvjiage_shuru6.insert(0, "0")  # 在输入框索引 0 的位置插入 "0"

    guolvjiage_shuru7 = tk.Entry(root, width=20)
    guolvjiage_shuru7.grid(row=7, column=3, padx=5, pady=5)
    guolvjiage_shuru7.insert(0, "0")  # 在输入框索引 0 的位置插入 "0"

    guolvjiage_shuru8 = tk.Entry(root, width=20)
    guolvjiage_shuru8.grid(row=7, column=4, padx=5, pady=5)
    guolvjiage_shuru8.insert(0, "0")  # 在输入框索引 0 的位置插入 "0"
    ############定时休息###########################################

    shijian = tk.Label(root, text="休息时间（时）:")
    shijian.grid(row=8, column=0, padx=5, pady=5)
    shijian_shuru = tk.Entry(root, width=20)
    shijian_shuru.grid(row=8, column=1, padx=5, pady=5)
    shijian_shuru.insert(0, "0")  # 在输入框索引 0 的位置插入 "0"

    shichang = tk.Label(root, text="休息时长（小时）")
    shichang.grid(row=8, column=2, padx=5, pady=5)
    shichang_shuru = tk.Entry(root, width=20)
    shichang_shuru.grid(row=8, column=3, padx=5, pady=5)
    shichang_shuru.insert(0, "0")  # 在输入框索引 0 的位置插入 "0"

    # 第八行###########################################################################

    cailiaogeshu = tk.Label(root, text="材料个数上限:")
    cailiaogeshu.grid(row=9, column=0, padx=5, pady=5)
    # 上限个数
    cailiaogeshu_shuru = tk.Entry(root, width=20)
    cailiaogeshu_shuru.grid(row=9, column=1, padx=5, pady=5)
    cailiaogeshu_shuru.insert(0, "1")  # 在输入框索引 0 的位置插入 "0"
    cailiaogeshu_shuru1 = tk.Entry(root, width=20)
    cailiaogeshu_shuru1.grid(row=9, column=2, padx=5, pady=5)
    cailiaogeshu_shuru1.insert(0, "3000")  # 在输入框索引 0 的位置插入 "0"

    sousuocishu = tk.Label(root, text="搜索次数:")
    sousuocishu.grid(row=10, column=0, padx=5, pady=5)
    # 上限个数
    sousuocishu_shuru = tk.Entry(root, width=20)
    sousuocishu_shuru.grid(row=10, column=1, padx=5, pady=5)
    sousuocishu_shuru.insert(0, "1")  # 在输入框索引 0 的位置插入 "0"

    sousuoshijian = tk.Label(root, text="搜索时间（/小时）:")
    sousuoshijian.grid(row=10, column=2, padx=5, pady=5)
    # 上限个数
    sousuoshijian_shuru = tk.Entry(root, width=20)
    sousuoshijian_shuru.grid(row=10, column=3, padx=5, pady=5)
    sousuoshijian_shuru.insert(0, "1")  # 在输入框索引 0 的位置插入 "0"

    #  分割线
    separator = ttk.Separator(root, orient='horizontal')
    separator.grid(row=12, column=0, columnspan=6, sticky='ew', padx=5, pady=5)

    # 材料记录地址
    cailiao = tk.Entry(root)
    cailiao.grid(row=13, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
    root.columnconfigure(0, minsize=200)

    # 创建选择文件按钮
    cailiao_button = tk.Button(root, text="价格保存/读取地址", command=cailiao_file)
    cailiao_button.grid(row=13, column=2, padx=5, pady=5)

    #  分割线
    separator = ttk.Separator(root, orient='horizontal')
    separator.grid(row=14, column=0, columnspan=6, sticky='ew', padx=5, pady=5)

    # 第九行###########################################################################
    # 上架
    shangjiageshu = tk.Label(root, text="最大上架个数:")
    shangjiageshu.grid(row=15, column=0, padx=5, pady=5)
    # 间隔时间输入框
    shangjiageshu_shuru = tk.Entry(root, width=20)
    shangjiageshu_shuru.grid(row=15, column=1, padx=5, pady=5)
    shangjiageshu_shuru.insert(0, "25")  # 在输入框索引 0 的位置插入 "25"

    jiageshangxian = tk.Label(root, text="单个价格上限:")
    jiageshangxian.grid(row=16, column=0, padx=5, pady=5)
    jiageshangxian_shuru = tk.Entry(root, width=20)
    jiageshangxian_shuru.grid(row=16, column=1, padx=5, pady=5)
    jiageshangxian_shuru.insert(0, "1000")  # 在输入框索引 0 的位置插入 "25"

    shangjia_button = tk.Button(root, text="开始上架", command=start_shangjia, bg="#808080", relief=tk.RAISED,
                                borderwidth=3,
                                font=("宋体", 15))
    shangjia_button.grid(row=15, column=4, rowspan=5, columnspan=2, padx=5, pady=5, sticky="nsew")
    root.columnconfigure(4, minsize=60)
    root.columnconfigure(5, minsize=60)
    root.rowconfigure(15, minsize=30)
    root.rowconfigure(16, minsize=30)

    # 是否需要出售装备
    shifouchushou = tk.IntVar()
    checkbox3 = tk.Checkbutton(root, text="出售装备", variable=shifouchushou)
    checkbox3.grid(row=17, column=0, padx=5, pady=5)

    # 下架相同装备
    xiajiaxiangtong = tk.IntVar()
    checkbox4 = tk.Checkbutton(root, text="下架相同装备", variable=xiajiaxiangtong)
    checkbox4.grid(row=17, column=1, padx=5, pady=5)

    # 配置列和行的权重，使按钮能根据窗口大小自适应
    for i in range(6):
        root.columnconfigure(i, weight=1)
    for i in range(17):
        root.rowconfigure(i, weight=1)

    # 加载配置
    load_config()

    # 运行主循环
    # root.mainloop()

    # 开始监听键盘事件
    with keyboard.Listener(on_press=on_press) as listener:
        root.mainloop()
