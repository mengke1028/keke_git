import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from snap7 import client, util
from snap7.types import Areas

plc_client = client.Client()

area = Areas.DB
stop = False
stop2 = False


def parse_db_address(address):
    """解析格式"""
    # 检查输入格式
    if not address.startswith("DB"):
        raise ValueError("地址必须以'DB'开头")
    try:
        db_part = address.split(".")
        database_number = int(db_part[0][2:])  # dbNo
        byte_offset = int(db_part[1][3:])  # 起始位置 start
        bit_index = int(db_part[2][-1])  # 索引位置
        return database_number, byte_offset, bit_index
    except ValueError:
        raise ValueError("地址格式不正确，无法解析")


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
    ip = plc_ip_entry.get()
    rack = 0
    slot = 1
    # 创建并连接到PLC
    try:
        plc_client.connect(ip, rack, slot)

        if plc_client.get_connected():
            messagebox.showinfo("连接通知", '和PLC建立连接成功')
            connect_button.config(style="Green.TButton")
            button1.config(state=tk.NORMAL)
            button2.config(state=tk.NORMAL)
            button3.config(state=tk.NORMAL)
            button4.config(state=tk.NORMAL)
            button5.config(state=tk.NORMAL)
            button6.config(state=tk.NORMAL)
            button7.config(state=tk.NORMAL)
            button8.config(state=tk.NORMAL)
            final_button.config(state=tk.NORMAL)
            set_mode()
            # 创建家具检测线程
            thread = threading.Thread(target=check_all_signal)
            thread.daemon = True  # 设置为守护线程
            # 启动线程
            thread.start()
    except:
        messagebox.showinfo("连接通知", '和PLC建立连接失败')


def down_normal_mode():
    """下压气缸原位 DB360.DBX2.1"""
    global stop2
    area = Areas.DB
    dbNo = 360
    start = 2
    stop2 = True
    time.sleep(0.05)
    try:
        current_val = plc_client.read_area(area, dbNo, start, 1)
        set_val = set_bit(current_val[0], 1)
        plc_client.write_area(area, dbNo, start, set_val.to_bytes(1, 'big'))
        time.sleep(0.05)
        clear_val = clear_bit(current_val[0], 1)
        plc_client.write_area(area, dbNo, start, clear_val.to_bytes(1, 'big'))
    except:
        pass
    stop2 = False


def down_work_mode():
    """下压气缸工作位 DB360.DBX2.2"""
    global stop2
    area = Areas.DB
    dbNo = 360
    start = 2
    stop2 = True
    time.sleep(0.05)
    try:
        current_val = plc_client.read_area(area, dbNo, start, 1)
        set_val = set_bit(current_val[0], 2)
        plc_client.write_area(area, dbNo, start, set_val.to_bytes(1, 'big'))
        time.sleep(0.05)
        clear_val = clear_bit(current_val[0], 2)
        plc_client.write_area(area, dbNo, start, clear_val.to_bytes(1, 'big'))
    except:
        pass
    stop2 = False


def scan_normal_mode():
    """扫码枪原位 DB360.DBX2.3 """
    global stop2
    area = Areas.DB
    dbNo = 360
    start = 2
    stop2 = True
    time.sleep(0.05)
    try:
        current_val = plc_client.read_area(area, dbNo, start, 1)
        set_val = set_bit(current_val[0], 3)
        plc_client.write_area(area, dbNo, start, set_val.to_bytes(1, 'big'))
        time.sleep(0.01)
        clear_val = clear_bit(current_val[0], 3)
        plc_client.write_area(area, dbNo, start, clear_val.to_bytes(1, 'big'))
    except:
        pass
    stop2 = False


def scan_work_mode():
    """扫码枪工作位 DB360.DBX2.4"""
    global stop2
    area = Areas.DB
    dbNo = 360
    start = 2
    stop2 = True
    time.sleep(0.05)
    try:
        current_val = plc_client.read_area(area, dbNo, start, 1)
        set_val = set_bit(current_val[0], 4)
        plc_client.write_area(area, dbNo, start, set_val.to_bytes(1, 'big'))
        time.sleep(0.01)
        clear_val = clear_bit(current_val[0], 4)
        plc_client.write_area(area, dbNo, start, clear_val.to_bytes(1, 'big'))
    except:
        pass
    stop2 = False


def stop_buzzer():
    """蜂鸣器屏蔽 DB360.DBX2.5 """
    global stop2
    area = Areas.DB
    dbNo = 360
    start = 2
    stop2 = True
    time.sleep(0.05)
    if not get_bool("DB360.DBX2.5"):
        try:
            current_val = plc_client.read_area(area, dbNo, start, 1)
            set_val = set_bit(current_val[0], 5)
            plc_client.write_area(area, dbNo, start, set_val.to_bytes(1, 'big'))
        except:
            pass
    else:
        try:
            current_val = plc_client.read_area(area, dbNo, start, 1)
            clear_val = clear_bit(current_val[0], 5)
            plc_client.write_area(area, dbNo, start, clear_val.to_bytes(1, 'big'))
        except:
            pass
    stop2 = False


def stop_door():
    """门屏蔽 DB360.DBX2.6 """
    global stop2
    area = Areas.DB
    dbNo = 360
    start = 2
    stop2 = True
    time.sleep(0.05)
    if not get_bool("DB360.DBX2.6"):
        try:
            current_val = plc_client.read_area(area, dbNo, start, 1)
            set_val = set_bit(current_val[0], 6)
            plc_client.write_area(area, dbNo, start, set_val.to_bytes(1, 'big'))
        except:
            pass
    else:
        try:
            current_val = plc_client.read_area(area, dbNo, start, 1)

            clear_val = clear_bit(current_val[0], 6)
            plc_client.write_area(area, dbNo, start, clear_val.to_bytes(1, 'big'))
        except:
            pass

    stop2 = False


def set_mode():
    """手动模式 DB360.DBX1.3 """

    mode = get_mode()
    if mode:
        button7.config(style="Green.TButton")
        button1.config(state=tk.DISABLED)
        button2.config(state=tk.DISABLED)
        button3.config(state=tk.DISABLED)
        button4.config(state=tk.DISABLED)

        button7.config(text="自动")
    else:
        button7.config(style="Custom.TButton")
        button7.config(text="手动")
        button1.config(state=tk.NORMAL)
        button2.config(state=tk.NORMAL)
        button3.config(state=tk.NORMAL)
        button4.config(state=tk.NORMAL)


def get_mode():
    """获取手动、自动模式的状态"""
    global stop2
    area = Areas.DB
    dbNo = 360
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
    """自动模式DB360.DBX1.3"""
    global stop2
    mode = get_mode()
    area = Areas.DB
    dbNo = 360
    start = 1
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
        print('是自动模式')
    else:
        print('是手动模式')


def initialization():
    """初始化 DB360.DBX1.5 """
    global stop2
    area = Areas.DB
    dbNo = 360
    start = 1
    stop2 = True
    time.sleep(0.05)
    stop_1()
    try:
        current_val = plc_client.read_area(area, dbNo, start, 1)

        set_val = set_bit(current_val[0], 5)
        plc_client.write_area(area, dbNo, start, set_val.to_bytes(1, 'big'))
        time.sleep(4)
        clea = clear_bit(current_val[0], 5)
        plc_client.write_area(area, dbNo, start, clea.to_bytes(1, 'big'))
        messagebox.showinfo("初始化通知", '初始化成功')
        button1.config(state=tk.NORMAL)
        button2.config(state=tk.NORMAL)
        button3.config(state=tk.NORMAL)
        button4.config(state=tk.NORMAL)
        button5.config(state=tk.NORMAL)
        button6.config(state=tk.NORMAL)
        button7.config(state=tk.NORMAL)
        button8.config(state=tk.NORMAL)
        final_button.config(state=tk.NORMAL)

    except:
        pass
    stop2 = False


def stop_all_button():
    """扫描全部按钮状态"""
    if get_bool("DB300.DBX4.1"):
        button1.config(style="Green.TButton")
    else:
        button1.config(style="Custom.TButton")

    if get_bool("DB300.DBX4.2"):
        button2.config(style="Green.TButton")
    else:
        button2.config(style="Custom.TButton")

    if get_bool("DB300.DBX4.3"):
        button3.config(style="Green.TButton")
    else:
        button3.config(style="Custom.TButton")

    if get_bool("DB300.DBX4.4"):
        button4.config(style="Green.TButton")
    else:
        button4.config(style="Custom.TButton")

    if get_bool("DB360.DBX2.5"):
        button5.config(style="Green.TButton")
    else:
        button5.config(style="Custom.TButton")

    if get_bool("DB360.DBX2.6"):
        button6.config(style="Green.TButton")
    else:
        button6.config(style="Custom.TButton")

    if get_bool("DB360.DBX1.1"):
        button8.config(style="Green.TButton")
    else:
        button8.config(style="Custom.TButton")
    set_mode()


def stop_1():
    button1.config(state=tk.DISABLED)
    button2.config(state=tk.DISABLED)
    button3.config(state=tk.DISABLED)
    button4.config(state=tk.DISABLED)
    button5.config(state=tk.DISABLED)
    button6.config(state=tk.DISABLED)
    button7.config(state=tk.DISABLED)
    button8.config(state=tk.DISABLED)
    final_button.config(state=tk.DISABLED)


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


def dengguang():
    """开关灯"""
    area = Areas.DB
    dbNo = 360
    start = 1
    time.sleep(0.05)
    if get_bool("DB360.DBX1.1"):
        try:
            current_val = plc_client.read_area(area, dbNo, start, 1)
            clear_val = clear_bit(current_val[0], 1)
            plc_client.write_area(area, dbNo, start, clear_val.to_bytes(1, 'big'))
        except:
            pass

    else:
        try:
            current_val = plc_client.read_area(area, dbNo, start, 1)
            set_val = set_bit(current_val[0], 1)
            plc_client.write_area(area, dbNo, start, set_val.to_bytes(1, 'big'))
        except:
            pass


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
            size = 11
            current_val = plc_client.read_area(area, dbNo, start, size)
            current_val_350 = plc_client.read_area(area, 350, start, 4)
        except:
            time.sleep(1)
            continue
        signal_list = [
            ("DB300.DBX4.1", xiaya_yuan),
            ("DB300.DBX4.2", xiaya_gongzuo),
            ("DB300.DBX4.3", saoma_yuan),
            ("DB300.DBX4.4", saoma_gongzuo),
            ("DB300.DBX4.5", jiaju_daowei),
            ("DB300.DBX4.6", ID0),
            ("DB300.DBX4.7", ID1),
            ("DB300.DBX5.0", ID2),
            ("DB300.DBX10.4", Press_signal1),
            ("DB300.DBX10.5", Press_signal2),
            ("DB300.DBX10.6", Press_signal3),
            ("DB300.DBW2", shebei),
            ("DB300.DBW6.0", baojing1),
            ("DB300.DBW8.0", baojing2),
            ("DB350.DBX0.7", test_start),
            ("DB350.DBX0.5", saoma_OK),
            ("DB350.DBX0.6", saoma_fail),
            ("DB350.DBX1.7", test_OK),
            ("DB350.DBX2.0", test_NG)
        ]
        for signal in signal_list:

            if "DB350" in signal[0]:
                database_number, byte_offset, bit_index = parse_db_address(signal[0])
                bool_val = util.get_bool(current_val_350, byte_offset, bit_index)

                if bool_val:
                    signal[1].config(bg='green')
                else:
                    signal[1].config(bg='grey')

                if "DB350.DBX2.0" == signal[0]:
                    if bool_val:
                        signal[1].config(bg='red')
                    else:
                        signal[1].config(bg='grey')
                if "DB350.DBX0.6" == signal[0]:
                    if bool_val:
                        signal[1].config(bg='red')
                    else:
                        signal[1].config(bg='grey')

            elif "X" in signal[0]:
                database_number, byte_offset, bit_index = parse_db_address(signal[0])
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
                warning1 = ["备用",
                            "急停被按下",
                            "安全门被打开",
                            "气压低",
                            "请求测试超时",
                            "扫码超时",
                            "F压板错误",
                            "L压板错误",
                            "R压板错误",
                            "备用",
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
                warning2 = ["下压气缸原位报警",
                            "下压气缸工作位报警",
                            "扫码气缸原位报警",
                            "扫码气缸工作位报警",
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

        time.sleep(0.5)


# 创建主窗口
root = tk.Tk()
root.title("PLC TEST—FCT")
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
button1 = ttk.Button(root, text="下压气缸原位", command=down_normal_mode, width=12)
button1.grid(row=1, column=0, padx=10, pady=5)

button2 = ttk.Button(root, text="下压气缸工作位", command=down_work_mode, width=12)
button2.grid(row=1, column=1, padx=10, pady=5)

ID0 = tk.Label(root, bg='grey', text="夹具FRONI", padx=10, pady=5, width=12)
ID0.grid(row=1, column=2, padx=10, pady=5)

ID1 = tk.Label(root, bg='grey', text="夹具LEFT", padx=10, pady=5, width=12)
ID1.grid(row=1, column=3, padx=10, pady=5)

ID2 = tk.Label(root, bg='grey', text="夹具RIGHT", padx=10, pady=5, width=12)
ID2.grid(row=1, column=4, padx=10, pady=5)

# 第三行的按钮
button3 = ttk.Button(root, text="扫码枪原位", command=scan_normal_mode, width=12)
button3.grid(row=2, column=0, padx=10, pady=5)

button4 = ttk.Button(root, text="扫码枪工作位", command=scan_work_mode, width=12)
button4.grid(row=2, column=1, padx=10, pady=5)

Press_signal1 = tk.Label(root, bg='grey', text="压板FRONT", padx=10, pady=5, width=12)
Press_signal1.grid(row=2, column=2, padx=10, pady=5)

Press_signal2 = tk.Label(root, bg='grey', text="压板LEFT", padx=10, pady=5, width=12)
Press_signal2.grid(row=2, column=3, padx=10, pady=5)

Press_signal3 = tk.Label(root, bg='grey', text="压板RIGHT", padx=10, pady=5, width=12)
Press_signal3.grid(row=2, column=4, padx=10, pady=5)

# 第四行的按钮
button5 = ttk.Button(root, text="蜂鸣器屏蔽", command=stop_buzzer, width=12)
button5.grid(row=3, column=0, padx=10, pady=5)

button6 = ttk.Button(root, text="门屏蔽", command=stop_door, width=12)
button6.grid(row=3, column=1, padx=10, pady=5)

xiaya_yuan = tk.Label(root, bg='grey', text="下压气缸原位", padx=10, pady=5, width=12)
xiaya_yuan.grid(row=3, column=2, padx=10, pady=5)

xiaya_gongzuo = tk.Label(root, bg='grey', text="下压气缸工作", padx=10, pady=5, width=12)
xiaya_gongzuo.grid(row=3, column=3, padx=10, pady=5)

saoma_yuan = tk.Label(root, bg='grey', text="扫码枪原位", padx=10, pady=5, width=12)
saoma_yuan.grid(row=3, column=4, padx=10, pady=5)

# 第五行的按钮
button7 = ttk.Button(root, text="手动", command=automatic, width=12)
button7.grid(row=4, column=0, padx=10, pady=5)

button8 = ttk.Button(root, text="灯光", command=dengguang, width=12)
button8.grid(row=4, column=1, padx=10, pady=5)

saoma_gongzuo = tk.Label(root, bg='grey', text="扫码枪工作位", padx=10, pady=5, width=12)
saoma_gongzuo.grid(row=4, column=2, padx=10, pady=5)

jiaju_daowei = tk.Label(root, bg='grey', text="夹具到位信号", padx=10, pady=5, width=12)
jiaju_daowei.grid(row=4, column=3, padx=10, pady=5)

baojing1 = tk.Label(root, bg='grey', text="报警信号1", padx=10, pady=5, width=12)
baojing1.grid(row=4, column=4, padx=10, pady=5)

# 第六行的按钮
final_button = ttk.Button(root, text="初始化, 等待4秒", command=initialization, width=30)  # 设置按钮宽度为20
final_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5)  # 横跨两列居中

baojing2 = tk.Label(root, bg='grey', text="报警信号2", padx=10, pady=5, width=12)
baojing2.grid(row=5, column=2, padx=14, pady=5)

shebei = tk.Label(root, bg='grey', text="设备状态", padx=10, pady=5, width=12)
shebei.grid(row=5, column=3, padx=14, pady=5)

test_start = tk.Label(root, bg='grey', text="开始测试", padx=10, pady=5, width=12)
test_start.grid(row=5, column=4, padx=14, pady=5)

saoma_OK = tk.Label(root, bg='grey', text="扫码OK", padx=10, pady=5, width=12)
saoma_OK.grid(row=6, column=2, padx=14, pady=5)

saoma_fail = tk.Label(root, bg='grey', text="扫码NG", padx=10, pady=5, width=12)
saoma_fail.grid(row=6, column=3, padx=14, pady=5)

test_OK = tk.Label(root, bg='grey', text="测试OK", padx=10, pady=5, width=12)
test_OK.grid(row=6, column=4, padx=14, pady=5)

test_NG = tk.Label(root, bg='grey', text="测试NG", padx=10, pady=5, width=12)
test_NG.grid(row=7, column=2, padx=14, pady=5)

# 运行主循环
stop_1()
root.mainloop()
