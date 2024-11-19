import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from snap7 import client, util
from snap7.types import Areas

import os
import logging
from datetime import datetime


def setup_logging():
    # 获取当前日期作为日志目录名称
    log_dir = f"PLC_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # 如果日志目录不存在，则创建它
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(script_dir+"\\"+log_dir):
        os.makedirs(log_dir)


    # 设置日志配置
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_dir, "app.log")),  # 将日志写入到文件
            logging.StreamHandler()  # 同时打印到控制台
        ]
    )


setup_logging()
plc_client = client.Client()

area = Areas.DB
stop = False
stop2 = False


def parse_db_address(address):
    """解析格式"""
    # 检查输入格式 DB300.DBX0.1
    if not address.startswith("DB"):
        raise ValueError("地址必须以'DB'开头")
    db_part = address.split(".")
    database_number = int(db_part[0][2:])  # dbNo
    byte_offset = int(db_part[1][3:])  # 起始位置 start
    bit_index = int(db_part[2][-1])  # 索引位置
    return database_number, byte_offset, bit_index


def clear_bit(value, bit_index):
    """清除一个字节中指定位的值（设为0）"""
    # 创建一个全1的掩码，然后左移要清除的位数，并取反，得到只清除指定位的掩码
    mask = ~(1 << bit_index)
    # 应用掩码清除指定位
    return value & mask


def set_bit(value, bit_index):
    """设置一个字节中指定位的值（设为1）"""
    # 创建一个只在指定位为1的掩码
    mask = 1 << bit_index
    # 应用掩码设置指定位
    return value | mask


def create_custom_styles(style_name, bg_color, fg_color):
    """创建自定义样式"""
    style = ttk.Style()
    style.element_create(style_name, "from", "default")
    style.layout(style_name, [
        (style_name, {"sticky": "nswe", "children": [
            (f"{style_name}.focus", {"sticky": "nswe", "children": [
                (f"{style_name}.padding", {"sticky": "nswe", "children": [
                    (f"{style_name}.label", {"sticky": "nswe"})
                ]})
            ]})
        ]})
    ])
    style.configure(style_name, background=bg_color, foreground=fg_color)


def on_connect_click():
    global plc_client, thread, PLC_connect_th, stop
    # 在这里添加连接到PLC的逻辑
    stop = False
    logging.info("连接按钮被点击，IP地址:", plc_ip_entry.get())
    ip = plc_ip_entry.get()
    rack = 0
    slot = 1
    # 创建并连接到PLC
    plc_client.connect(ip, rack, slot)

    if plc_client.get_connected():
        messagebox.showinfo("连接通知", '和PLC建立连接成功')
        logging.info("和PLC建立连接成功")
        connect_button.config(style="Green.TButton")
        stop_all_button()
        # FRONT.config(state=tk.NORMAL)
        # LEFT.config(state=tk.NORMAL)
        disconnect_button.config(state=tk.NORMAL)
        # RIGHT.config(state=tk.NORMAL)
        button7.config(state=tk.NORMAL)
        final_button.config(state=tk.NORMAL)
        # 创建家具检测线程
        thread = threading.Thread(target=check_all_signal)
        thread.daemon = True  # 设置为守护线程
        # 启动线程
        thread.start()
        logging.info("启动线程")


def test_front():
    """测试FRONT DB350.DBX0.1"""
    global stop2

    area = Areas.DB
    dbNo = 350
    start = 1
    stop2 = True
    time.sleep(0.05)
    if get_bool("DB350.DBX0.1"):
        current_val = plc_client.read_area(area, dbNo, start, 1)
        clear_val = clear_bit(current_val[0], 1)
        plc_client.write_area(area, dbNo, start, clear_val.to_bytes(1, 'big'))
    else:
        current_val = plc_client.read_area(area, dbNo, start, 1)
        set_val = set_bit(current_val[0], 1)
        plc_client.write_area(area, dbNo, start, set_val.to_bytes(1, 'big'))

    stop2 = False


def test_left():
    """测试FRONT DB350.DBX0.2"""
    global stop2
    area = Areas.DB
    dbNo = 350
    start = 1
    stop2 = True
    time.sleep(0.05)
    if get_bool("DB350.DBX0.2"):
        current_val = plc_client.read_area(area, dbNo, start, 1)
        clear_val = clear_bit(current_val[0], 1)
        plc_client.write_area(area, dbNo, start, clear_val.to_bytes(1, 'big'))
    else:
        current_val = plc_client.read_area(area, dbNo, start, 1)
        set_val = set_bit(current_val[0], 1)
        plc_client.write_area(area, dbNo, start, set_val.to_bytes(1, 'big'))
    stop2 = False


def test_right():
    """蜂鸣器屏蔽 DB350.DBX0.3 """
    global stop2
    area = Areas.DB
    dbNo = 350
    start = 1
    stop2 = True
    time.sleep(0.05)
    if get_bool("DB350.DBX0.3"):
        current_val = plc_client.read_area(area, dbNo, start, 1)
        clear_val = clear_bit(current_val[0], 1)
        plc_client.write_area(area, dbNo, start, clear_val.to_bytes(1, 'big'))
    else:
        current_val = plc_client.read_area(area, dbNo, start, 1)
        set_val = set_bit(current_val[0], 1)
        plc_client.write_area(area, dbNo, start, set_val.to_bytes(1, 'big'))
    stop2 = False


def set_mode():
    """手动模式 DB350.DBX1.3 """

    mode = get_mode()

    if mode:
        button7.config(style="Green.TButton")

        button7.config(text="自动")
    else:
        button7.config(style="Custom.TButton")
        button7.config(text="手动")


def get_mode():
    """获取手动、自动模式的状态"""
    global stop2
    area = Areas.DB
    dbNo = 350
    start = 1
    size = 1
    stop2 = True
    time.sleep(0.05)
    try:
        byteRet = plc_client.read_area(area, dbNo, start, size)
        value = byteRet[0]
        bit_6_set = (value >> 3) & 1  # 右移5位，然后与1进行按位与操作来检测该位是否为1
        mode = bool(bit_6_set)
        stop2 = False
        return mode
    except:
        pass
    stop2 = False


def automatic():
    """自动模式DB350.DBX1.3"""
    global stop2
    area = Areas.DB
    dbNo = 350
    start = 1
    mode = get_mode()
    stop2 = True
    time.sleep(0.05)
    if mode:
        try:
            current_val = plc_client.read_area(area, dbNo, start, 1)
            clear = clear_bit(current_val[0], 3)
            plc_client.write_area(area, dbNo, start, clear.to_bytes(1, 'big'))
        except:
            pass

    else:
        try:
            current_val = plc_client.read_area(area, dbNo, start, 1)
            set = set_bit(current_val[0], 3)
            plc_client.write_area(area, dbNo, start, set.to_bytes(1, 'big'))
        except:
            pass

    stop2 = False

    mode = get_mode()
    if mode:
        button7.config(style="Green.TButton")
        button7.config(text="自动")
    else:
        button7.config(style="Custom.TButton")
        button7.config(text="手动")


def initialization():
    """初始化 DB350.DBX1.5 """
    global stop2
    area = Areas.DB
    dbNo = 350
    start = 1
    stop2 = True
    time.sleep(0.05)
    try:
        current_val = plc_client.read_area(area, dbNo, start, 1)
        set_val = set_bit(current_val[0], 5)
        plc_client.write_area(area, dbNo, start, set_val.to_bytes(1, 'big'))
        time.sleep(4)
        clea = clear_bit(current_val[0], 5)
        plc_client.write_area(area, dbNo, start, clea.to_bytes(1, 'big'))
        messagebox.showinfo("初始化通知", '初始化成功')
    except:
        pass
    stop2 = False


def stop_all_button():
    """扫描全部按钮状态"""
    # if get_bool("DB300.DBX0.1"):  # 读取测试产品ID0
    #     FRONT.config(style="Green.TButton")
    # else:
    #     FRONT.config(style="Custom.TButton")
    #
    # if get_bool("DB300.DBX0.2"):  # 读取测试产品ID1
    #     LEFT.config(style="Green.TButton")
    # else:
    #     LEFT.config(style="Custom.TButton")
    #
    # if get_bool("DB300.DBX0.3"):  # 读取测试产品ID2
    #     RIGHT.config(style="Green.TButton")
    # else:
    #     RIGHT.config(style="Custom.TButton")

    # set_mode()
    if get_bool("DB350.DBX1.3"):  # 读取手动/自动状态信号
        button7.config(style="Green.TButton")
        button7.config(text="自动")
    else:
        button7.config(style="Custom.TButton")
        button7.config(text="手动")


def stop_1():
    # FRONT.config(state=tk.DISABLED)
    # LEFT.config(state=tk.DISABLED)
    # RIGHT.config(state=tk.DISABLED)
    button7.config(state=tk.DISABLED)
    final_button.config(state=tk.DISABLED)
    disconnect_button.config(state=tk.DISABLED)


##########################################################################################

def get_bool(data):
    database_number, byte_offset, bit_index = parse_db_address(data)
    try:
        byteRet = plc_client.read_area(area, database_number, byte_offset, 1)
    except:
        return None
    value = byteRet[0]
    bit_6_set = (value >> bit_index) & 1
    mode = bool(bit_6_set)
    return mode


def disconnect():
    """断开连接"""
    global thread, PLC_connect_th, stop
    stop = True
    time.sleep(1)
    plc_client.disconnect()
    messagebox.showinfo("连接通知", '和PLC断开成功')

    connect_button.config(style="Gray.TButton")


def check_all_signal():
    while True:
        if stop:
            return
        if stop2:
            time.sleep(1)
            continue
        stop_all_button()
        try:
            area = Areas.DB
            dbNo = 300
            start = 0  # 从DB的第2个字节开始，对应于DBX2
            size = 13
            current_val = plc_client.read_area(area, dbNo, start, size)
            time.sleep(0.1)
            current_val_350 = plc_client.read_area(area, 350, start, 5)
        except:
            time.sleep(1)
            continue
        signal_list = [("DB300.DBX4.5", jiaju_daowei),
                       ("DB300.DBX4.6", ID0),
                       ("DB300.DBX4.7", ID1),
                       ("DB300.DBX5.0", ID2),
                       ("DB300.DBX5.1", yaban),
                       ("DB300.DBX12.0", gongwei1),
                       ("DB300.DBX12.1", gongwei2),
                       ("DB300.DBX12.2", gongwei3),
                       ("DB300.DBX12.3", gongwei4),
                       ("DB300.DBX12.4", gongwei5),
                       ("DB300.DBX12.5", gongwei6),
                       ("DB300.DBX12.6", gongwei7),
                       ("DB300.DBX12.7", gongwei8),
                       ("DB300.DBW2", shebei),
                       ("DB350.DBX0.7", kaishceshi),
                       ("DB350.DBX1.0", ceshiwancheng),
                       ("DB350.DBX4.0", gongwei1_pass),
                       ("DB350.DBX4.1", gongwei1_fail),
                       ("DB350.DBX4.2", gongwei2_pass),
                       ("DB350.DBX4.3", gongwei2_fail),
                       ("DB350.DBX4.4", gongwei3_pass),
                       ("DB350.DBX4.5", gongwei3_fail),
                       ("DB350.DBX4.6", gongwei4_pass),
                       ("DB350.DBX4.7", gongwei4_fail),
                       ("DB350.DBX2.6", test1),
                       ("DB350.DBX2.7", test2),
                       ("DB350.DBX3.0", test3),
                       ("DB350.DBX3.1", test4)]

        for signal in signal_list:

            if "X" in signal[0]:
                database_number, byte_offset, bit_index = parse_db_address(signal[0])
                if "350" in signal[0]:
                    bool_val_350 = util.get_bool(current_val_350, byte_offset, bit_index)
                    if bool_val_350:
                        signal[1].config(bg='grey')
                        if signal[0] in ["DB350.DBX4.1", "DB350.DBX4.3", 'DB350.DBX4.5', 'DB350.DBX4.7']:
                            signal[1].config(bg='red')
                        if signal[0] in ["DB350.DBX4.2", "DB350.DBX4.4", 'DB350.DBX4.6', 'DB350.DBX4.7']:
                            signal[1].config(bg='green')
                    else:
                        signal[1].config(bg='grey')

                else:
                    bool_val = util.get_bool(current_val, byte_offset, bit_index)
                    if bool_val:
                        signal[1].config(bg='green')
                    else:
                        signal[1].config(bg='grey')

            elif "DB300.DBW2" == signal[0]:
                devices_mode = [(1, "手动中"), (2, "自动"), (4, "设备运行中"), (5, "设备报警中"), (6, "设备初始化中"), (7, "光栅被阻挡"),
                                (8, "门未关好"),
                                (9, "急停被按下")]
                int_val = util.get_int(current_val, 2)
                for mode in devices_mode:
                    if int_val in mode:
                        shebei.config(text=mode[1])

            elif "DB300.DBW6.0" == signal[0]:
                word_val = util.get_word(current_val, 6)
                binary_string = format(word_val, 'b')
                binary_string_list = list(binary_string)
                binary_string_list.reverse()
                warning1 = ["PC离线",
                            "急停被按下",
                            "安全门被打开",
                            "气压低",
                            "请求测试超时",
                            "扫码超时",
                            "夹具ID1错误",
                            "夹具ID21错误",
                            "夹具ID3错误",
                            "VPC连接器没到位",
                            "备用",
                            "备用",
                            "备用",
                            "备用",
                            "备用",
                            "备用"]
                for item, w1 in enumerate(binary_string_list):
                    if w1 == '1':
                        text = warning1[item]
                        baojing1.config(text=text, bg='red')
                    else:
                        baojing1.config(text="1无报警", bg='grey')

            elif "DB300.DBW8.0" == signal[0]:
                word_val = util.get_word(current_val, 8)
                binary_string = format(word_val, 'b')
                binary_string_list = list(binary_string)
                binary_string_list.reverse()
                warning2 = ["VPC气缸原位报警",
                            "VPC气缸工位报警",
                            "备用",
                            "备用",
                            "备用",
                            "备用",
                            "备用",
                            "备用",
                            "备用",
                            "备用",
                            "备用",
                            "备用",
                            "备用",
                            "备用",
                            "备用",
                            "备用", ]
                for item, w1 in enumerate(binary_string_list):
                    if w1 == '1':
                        text = warning2[item]
                        baojing2.config(text=text, bg='read')
                    else:
                        baojing2.config(text="1无报警", bg='grey')
        time.sleep(0.1)


def center_window(window, width, height):
    # 获取屏幕的宽度和高度
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # 计算窗口左上角的坐标
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # 设置窗口的位置
    window.geometry(f"{width}x{height}+{x}+{y}")


# 创建主窗口
root = tk.Tk()
# 设置窗口的宽度和高度
window_width = 750
window_height = 450

# 将窗口居中显示
# center_window(root, window_width, window_height)


root.title("PLC TEST-DSOS")
create_custom_styles("Gray.TButton", "#808080", "white")
create_custom_styles("Green.TButton", "green", "white")

# 第一行：PLC IP标签和文本框、连接按钮
plc_ip_label = ttk.Label(root, text="PLC IP:")
plc_ip_label.grid(row=0, column=0, padx=10, pady=5)

plc_ip_entry = ttk.Entry(root)
initial_ip_value = "192.168.1.200"
plc_ip_entry.insert(0, initial_ip_value)
plc_ip_entry.grid(row=0, column=1, padx=10, pady=5)

connect_button = ttk.Button(root, text="连接", command=on_connect_click)
connect_button.grid(row=0, column=2, padx=10, pady=5)

disconnect_button = ttk.Button(root, text="断开", command=disconnect)
disconnect_button.grid(row=0, column=3, padx=10, pady=5)

# 第二行的按钮
# FRONT = ttk.Button(root, text="产品FRONT", command=test_front, width=14)
# FRONT.grid(row=1, column=0, padx=10, pady=5)
#
# LEFT = ttk.Button(root, text="产品LEFT", command=test_left, width=14)
# LEFT.grid(row=1, column=1, padx=10, pady=5)

ID0 = tk.Label(root, bg='grey', text="夹具FRONI", padx=10, pady=5, width=14)
ID0.grid(row=1, column=2, padx=10, pady=5)

ID1 = tk.Label(root, bg='grey', text="夹具LEFT", padx=10, pady=5, width=14)
ID1.grid(row=1, column=3, padx=10, pady=5)

ID2 = tk.Label(root, bg='grey', text="夹具RIGHT", padx=10, pady=5, width=14)
ID2.grid(row=1, column=4, padx=10, pady=5)

# # 第三行的按钮
# button3 = ttk.Button(root, text="扫码枪原位", command=scan_normal_mode, width=14)
# button3.grid(row=2, column=0, padx=10, pady=5)
#
# button4 = ttk.Button(root, text="扫码枪工作位", command=scan_work_mode, width=14)
# button4.grid(row=2, column=1, padx=10, pady=5)
#
# Press_signal1 = tk.Label(root, bg='grey', text="压板FRONT", padx=10, pady=5, width=14)
# Press_signal1.grid(row=2, column=2, padx=10, pady=5)
#
# Press_signal2 = tk.Label(root, bg='grey', text="压板LEFT", padx=10, pady=5, width=14)
# Press_signal2.grid(row=2, column=3, padx=10, pady=5)
#
# Press_signal3 = tk.Label(root, bg='grey', text="压板RIGHT", padx=10, pady=5, width=14)
# Press_signal3.grid(row=2, column=4, padx=10, pady=5)

# 第四行的按钮
# RIGHT = ttk.Button(root, text="产品RIGHT", command=test_right, width=14)
# RIGHT.grid(row=3, column=0, padx=10, pady=5)

# button6 = ttk.Button(root, text="门屏蔽", command=stop_door, width=14)
# button6.grid(row=3, column=1, padx=10, pady=5)

yaban = tk.Label(root, bg='grey', text="压盖压到位信号", padx=10, pady=5, width=14)
yaban.grid(row=3, column=2, padx=10, pady=5)

shebei = tk.Label(root, bg='grey', text="设备状态", padx=10, pady=5, width=14)
shebei.grid(row=3, column=3, padx=14, pady=5)

# saoma_yuan = tk.Label(root, bg='grey', text="扫码枪原位", padx=10, pady=5, width=14)
# saoma_yuan.grid(row=3, column=4, padx=10, pady=5)

# 第五行的按钮
button7 = ttk.Button(root, text="手动", command=automatic, width=30)
button7.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

# button8 = ttk.Button(root, text="灯光", command=dengguang, width=14)
# button8.grid(row=4, column=1, padx=10, pady=5)

# saoma_gongzuo = tk.Label(root, bg='grey', text="扫码枪工作位", padx=10, pady=5, width=14)
# saoma_gongzuo.grid(row=4, column=2, padx=10, pady=5)

jiaju_daowei = tk.Label(root, bg='grey', text="夹具到位信号", padx=10, pady=5, width=14)
jiaju_daowei.grid(row=3, column=4, padx=10, pady=5)

baojing1 = tk.Label(root, bg='grey', text="报警信号1", padx=10, pady=5, width=14)
baojing1.grid(row=4, column=2, padx=10, pady=5)

# 第六行的按钮
final_button = ttk.Button(root, text="初始化，等待4秒", command=initialization, width=30)  # 设置按钮宽度为20
final_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)  # 横跨两列居中

baojing2 = tk.Label(root, bg='grey', text="报警信号2", padx=10, pady=5, width=14)
baojing2.grid(row=4, column=3, padx=14, pady=5)

gongwei1 = tk.Label(root, bg='grey', text="1工位产品到位信号1", padx=10, pady=5, width=14)
gongwei1.grid(row=4, column=4, padx=14, pady=5)

gongwei2 = tk.Label(root, bg='grey', text="1工位产品到位信号2", padx=10, pady=5, width=14)
gongwei2.grid(row=5, column=2, padx=14, pady=5)

gongwei3 = tk.Label(root, bg='grey', text="2工位产品到位信号1", padx=10, pady=5, width=14)
gongwei3.grid(row=5, column=3, padx=14, pady=5)

gongwei4 = tk.Label(root, bg='grey', text="2工位产品到位信号2", padx=10, pady=5, width=14)
gongwei4.grid(row=5, column=4, padx=14, pady=5)

gongwei5 = tk.Label(root, bg='grey', text="3工位产品到位信号1", padx=10, pady=5, width=14)
gongwei5.grid(row=6, column=2, padx=14, pady=5)

gongwei6 = tk.Label(root, bg='grey', text="3工位产品到位信号2", padx=10, pady=5, width=14)
gongwei6.grid(row=6, column=3, padx=14, pady=5)

gongwei7 = tk.Label(root, bg='grey', text="4工位产品到位信号1", padx=10, pady=5, width=14)
gongwei7.grid(row=6, column=4, padx=14, pady=5)

gongwei8 = tk.Label(root, bg='grey', text="4工位产品到位信号2", padx=10, pady=5, width=14)
gongwei8.grid(row=7, column=2, padx=14, pady=5)

kaishceshi = tk.Label(root, bg='grey', text="开始测试", padx=10, pady=5, width=14)
kaishceshi.grid(row=7, column=3, padx=14, pady=5)

ceshiwancheng = tk.Label(root, bg='grey', text="测试完成", padx=10, pady=5, width=14)
ceshiwancheng.grid(row=7, column=4, padx=14, pady=5)

gongwei1_pass = tk.Label(root, bg='grey', text="测试工位1结果pass", padx=10, pady=5, width=14)
gongwei1_pass.grid(row=8, column=2, padx=14, pady=5)

gongwei1_fail = tk.Label(root, bg='grey', text="测试工位1结果faile", padx=10, pady=5, width=14)
gongwei1_fail.grid(row=8, column=3, padx=14, pady=5)

gongwei2_pass = tk.Label(root, bg='grey', text="测试工位2结果pass", padx=10, pady=5, width=14)
gongwei2_pass.grid(row=8, column=4, padx=14, pady=5)

gongwei2_fail = tk.Label(root, bg='grey', text="测试工位2结果fail", padx=10, pady=5, width=14)
gongwei2_fail.grid(row=9, column=2, padx=14, pady=5)

gongwei3_pass = tk.Label(root, bg='grey', text="测试工位3结果pass", padx=10, pady=5, width=14)
gongwei3_pass.grid(row=9, column=3, padx=14, pady=5)

gongwei3_fail = tk.Label(root, bg='grey', text="测试工位3结果fail", padx=10, pady=5, width=14)
gongwei3_fail.grid(row=9, column=4, padx=14, pady=5)

gongwei4_pass = tk.Label(root, bg='grey', text="测试工位4结果pass", padx=10, pady=5, width=14)
gongwei4_pass.grid(row=10, column=2, padx=14, pady=5)

gongwei4_fail = tk.Label(root, bg='grey', text="测试工位4结果fail", padx=10, pady=5, width=14)
gongwei4_fail.grid(row=10, column=3, padx=14, pady=5)

test1 = tk.Label(root, bg='grey', text="测试工位1", padx=10, pady=5, width=14)
test1.grid(row=10, column=4, padx=14, pady=5)
test2 = tk.Label(root, bg='grey', text="测试工位2", padx=10, pady=5, width=14)
test2.grid(row=11, column=2, padx=14, pady=5)
test3 = tk.Label(root, bg='grey', text="测试工位3", padx=10, pady=5, width=14)
test3.grid(row=11, column=3, padx=14, pady=5)
test4 = tk.Label(root, bg='grey', text="测试工位4", padx=10, pady=5, width=14)
test4.grid(row=11, column=4, padx=14, pady=5)

# 运行主循环
stop_1()
root.mainloop()
