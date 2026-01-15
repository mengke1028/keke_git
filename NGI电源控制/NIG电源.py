import serial
import time
import logging
import re
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import queue

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ===================== 核心配置（可根据实际修改）=====================
ECU_COM_MAP = {
    "ECU1": "COM1",
    "ECU2": "COM1",
    "ECU3": "COM2",
    "ECU4": "COM2",
    "ECU5": "COM3",
    "ECU6": "COM3"
}
BAUD_RATE = 9600
# ====================================================================

class PowerSupply:
    def __init__(self, port, baud_rate=9600):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = None
        self.connect()

    def connect(self):
        """建立串口连接，增加异常处理"""
        try:
            if self.ser and self.ser.is_open:
                self.ser.close()
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=1)
            logging.info(f"成功连接串口 {self.port}")
            return True
        except Exception as e:
            logging.error(f"连接串口 {self.port} 失败: {str(e)}")
            return False

    def send_command(self, command):
        """发送指令，增加异常处理"""
        if not self.ser or not self.ser.is_open:
            if not self.connect():
                return False
        try:
            cmd = command.strip() + '\n'
            self.ser.write(cmd.encode("ascii"))
            logging.debug(f"发送指令: {cmd.strip()}")
            return True
        except Exception as e:
            logging.error(f"发送指令失败 {command}: {str(e)}")
            return False

    def send_ovp_ocp(self, channel, ovp, ocp):
        """设置过压过流保护"""
        cmd_ovp = f"PROT{channel}:VOLT {ovp}"
        self.send_command(cmd_ovp)
        ocp_mA = int(ocp) * 1000
        cmd_ocp = f"PROT{channel}:CURR {ocp_mA}"
        self.send_command(cmd_ocp)

    def set_voltage(self, channel, voltage):
        """设置输出电压"""
        command = f"SOURce{channel}:VOLTage {voltage}"
        result = self.send_command(command)
        time.sleep(0.1)
        self.flushAll()
        return result

    def set_current(self, channel, current):
        """设置输出电流"""
        command = f"SOURce{channel}:CURRent {current}"
        result = self.send_command(command)
        time.sleep(0.1)
        self.flushAll()
        return result

    def enable_output(self, channel, enable=True):
        """启用/禁用输出"""
        command = f"OUTPut{channel}:ONOFF {1 if enable else 0}"
        result = self.send_command(command)
        return result

    def read_data(self, query):
        """读取串口返回数据"""
        if not self.ser or not self.ser.is_open:
            if not self.connect():
                return ""
        try:
            self.send_command(query)
            response = self.ser.read_until('\n'.encode()).decode().strip()
            logging.debug(f"读取数据: {query} -> {response}")
            return response
        except Exception as e:
            logging.error(f"读取数据失败 {query}: {str(e)}")
            return ""

    def read_output_voltage(self, channel):
        """读取输出电压"""
        query = f"MEASure{channel}:VOLTage?"
        voltage_str = self.read_data(query)
        try:
            voltage_str = voltage_str.replace('V', '')
            voltage_str = re.sub(r'[^0-9.]', '', voltage_str)
            return float(voltage_str) if voltage_str else 0.0
        except:
            logging.error(f"解析电压失败: {voltage_str}")
            return 0.0

    def read_output_current(self, channel):
        """读取输出电流"""
        query = f"MEASure{channel}:CURRent?"
        current_str = self.read_data(query)
        try:
            current_str = current_str.replace('A', '')
            current_str = re.sub(r'[^0-9.]', '', current_str)
            return float(current_str) if current_str else 0.0
        except:
            logging.error(f"解析电流失败: {current_str}")
            return 0.0

    def read_enabled_state(self, channel):
        """读取输出开关状态"""
        query = f"OUTP{channel}:STATe?"
        enable_data = self.read_data(query)
        if enable_data == '33':
            return "开启"
        elif enable_data == '32':
            return "关闭"
        else:
            return f"未知({enable_data})"

    def flushAll(self):
        """清空串口缓冲区"""
        try:
            if self.ser and self.ser.in_waiting > 0:
                self.ser.read(self.ser.in_waiting)
        except:
            pass

    def close(self):
        """关闭串口"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            logging.info(f"关闭串口 {self.port}")

class ECUControllerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("6路ECU电源控制器（平铺版）")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)

        # 创建ttk样式，解决按钮颜色问题
        self.setup_ttk_styles()

        self.psu_instances = {}
        self.msg_queue = queue.Queue()

        self.setup_ui()
        self.update_ui_from_queue()

    def setup_ttk_styles(self):
        """创建ttk样式，定义按钮颜色"""
        style = ttk.Style(self.root)
        style.configure("Start.TButton", foreground="white", background="#2ca02c")
        style.configure("Stop.TButton", foreground="white", background="#d62728")
        # 鼠标悬浮效果
        style.map("Start.TButton",
                  background=[('active', '#28a745')],
                  foreground=[('active', 'white')])
        style.map("Stop.TButton",
                  background=[('active', '#dc3545')],
                  foreground=[('active', 'white')])

    def setup_ui(self):
        """构建UI：2行3列平铺6个ECU面板"""
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ecu_list = ["ECU1", "ECU2", "ECU3", "ECU4", "ECU5", "ECU6"]
        row_col_map = {
            "ECU1": (0, 0), "ECU2": (0, 1), "ECU3": (0, 2),
            "ECU4": (1, 0), "ECU5": (1, 1), "ECU6": (1, 2)
        }

        for ecu in ecu_list:
            row, col = row_col_map[ecu]
            ecu_frame = ttk.LabelFrame(main_frame, text=ecu, padding="10", labelanchor=tk.N)
            ecu_frame.grid(row=row, column=col, padx=8, pady=8, sticky=tk.NSEW)
            self.create_ecu_control_panel(ecu_frame, ecu)

        # 设置网格权重，自适应缩放
        for i in range(2):
            main_frame.grid_rowconfigure(i, weight=1)
        for j in range(3):
            main_frame.grid_columnconfigure(j, weight=1)

    def create_ecu_control_panel(self, parent, ecu_name):
        """创建单个ECU的控制面板"""
        # 串口信息
        com_ports = ECU_COM_MAP[ecu_name]
        print(com_ports)
        com_text = ", ".join(com_ports) if isinstance(com_ports, list) else com_ports
        ttk.Label(parent, text=f"对应串口：{com_text}", font=("Arial", 9, "bold")).grid(
            row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 8)
        )

        # 通道选择
        ttk.Label(parent, text="通道：", font=("Arial", 9)).grid(row=1, column=0, sticky=tk.E, padx=3, pady=3)
        if ecu_name in ['ECU1', 'ECU3', 'ECU5']:
            self.channel_var = tk.StringVar(value="1")
        elif ecu_name in ['ECU2', 'ECU4', 'ECU6']:
            self.channel_var = tk.StringVar(value="2")

        channel_combo = ttk.Combobox(parent, textvariable=self.channel_var, values=["1", "2"], width=6, state="readonly")
        channel_combo.grid(row=1, column=1, sticky=tk.W, padx=3, pady=3)
        setattr(self, f"{ecu_name}_channel_var", self.channel_var)

        # 电压设置 & 显示
        ttk.Label(parent, text="电压(V)：", font=("Arial", 9)).grid(row=2, column=0, sticky=tk.E, padx=3, pady=3)
        voltage_var = tk.StringVar(value="0.0")
        ttk.Entry(parent, textvariable=voltage_var, width=8, font=("Arial", 9)).grid(row=2, column=1, padx=3, pady=3)
        ttk.Button(parent, text="设置", command=lambda: self.set_ecu_param(ecu_name, "voltage", voltage_var.get()), width=6).grid(
            row=2, column=2, padx=3, pady=3
        )
        voltage_display = ttk.Label(parent, text="当前：-- V", font=("Arial", 9), foreground="#1f77b4")
        voltage_display.grid(row=2, column=3, padx=5, pady=3, sticky=tk.W)
        setattr(self, f"{ecu_name}_voltage_display", voltage_display)

        # 电流设置 & 显示
        ttk.Label(parent, text="电流(A)：", font=("Arial", 9)).grid(row=3, column=0, sticky=tk.E, padx=3, pady=3)
        current_var = tk.StringVar(value="0.0")
        ttk.Entry(parent, textvariable=current_var, width=8, font=("Arial", 9)).grid(row=3, column=1, padx=3, pady=3)
        ttk.Button(parent, text="设置", command=lambda: self.set_ecu_param(ecu_name, "current", current_var.get()), width=6).grid(
            row=3, column=2, padx=3, pady=3
        )
        current_display = ttk.Label(parent, text="当前：-- A", font=("Arial", 9), foreground="#ff7f0e")
        current_display.grid(row=3, column=3, padx=5, pady=3, sticky=tk.W)
        setattr(self, f"{ecu_name}_current_display", current_display)

        # 输出开关控制
        ttk.Button(parent, text="开启输出", command=lambda: self.toggle_ecu_output(ecu_name, True),
                   width=8, style="Start.TButton").grid(
            row=4, column=0, columnspan=2, padx=2, pady=5, sticky=tk.EW
        )
        ttk.Button(parent, text="关闭输出", command=lambda: self.toggle_ecu_output(ecu_name, False),
                   width=8, style="Stop.TButton").grid(
            row=4, column=2, columnspan=2, padx=2, pady=5, sticky=tk.EW
        )

        # ========== 核心修复：sticky参数修改 ==========
        # 将 sticky=tk.CENTER 改为 sticky="nsew"（实现居中效果）
        state_display = ttk.Label(parent, text="状态：--", font=("Arial", 9, "bold"), foreground="#9467bd")
        state_display.grid(row=5, column=0, columnspan=4, pady=3, sticky="nsew")  # 修复此处！
        setattr(self, f"{ecu_name}_state_display", state_display)

        # 刷新数据按钮
        ttk.Button(parent, text="刷新数据", command=lambda: self.read_ecu_data(ecu_name),
                   width=30).grid(row=6, column=0, columnspan=4, pady=8, sticky=tk.EW)

    def get_psu_instance(self, com_port):
        """获取/创建PowerSupply实例"""
        if com_port not in self.psu_instances:
            self.psu_instances[com_port] = PowerSupply(com_port, BAUD_RATE)
        return self.psu_instances[com_port]

    def set_ecu_param(self, ecu_name, param_type, value):
        """设置电压/电流（子线程）"""
        def worker():
            try:
                value_float = float(value)
                if value_float < 0:
                    raise ValueError("数值不能为负数")
                channel = int(getattr(self, f"{ecu_name}_channel_var").get())
                com_ports = ECU_COM_MAP[ecu_name]
                com_list = com_ports if isinstance(com_ports, list) else [com_ports]
                for com in com_list:
                    psu = self.get_psu_instance(com)
                    if param_type == "voltage":
                        psu.set_voltage(channel, value_float)
                    else:
                        psu.set_current(channel, value_float)
                self.msg_queue.put(("info", f"{ecu_name} {param_type}设置成功：{value}"))
                self.read_ecu_data(ecu_name, auto=True)
            except ValueError as e:
                self.msg_queue.put(("error", f"{ecu_name} 输入错误：{str(e)}"))
            except Exception as e:
                self.msg_queue.put(("error", f"{ecu_name} {param_type}设置失败：{str(e)}"))
        threading.Thread(target=worker, daemon=True).start()

    def toggle_ecu_output(self, ecu_name, enable):
        """开启/关闭输出（子线程）"""
        def worker():
            try:
                channel = int(getattr(self, f"{ecu_name}_channel_var").get())
                com_ports = ECU_COM_MAP[ecu_name]
                com_list = com_ports if isinstance(com_ports, list) else [com_ports]
                for com in com_list:
                    psu = self.get_psu_instance(com)
                    psu.enable_output(channel, enable)
                status = "开启" if enable else "关闭"
                self.msg_queue.put(("info", f"{ecu_name} 输出{status}成功"))
                self.read_ecu_data(ecu_name, auto=True)
            except Exception as e:
                self.msg_queue.put(("error", f"{ecu_name} 输出控制失败：{str(e)}"))
        threading.Thread(target=worker, daemon=True).start()

    def read_ecu_data(self, ecu_name, auto=False):
        """读取数据（子线程）"""
        def worker():
            try:
                channel = int(getattr(self, f"{ecu_name}_channel_var").get())
                com_ports = ECU_COM_MAP[ecu_name]
                com = com_ports[0] if isinstance(com_ports, list) else com_ports
                psu = self.get_psu_instance(com)
                voltage = psu.read_output_voltage(channel)
                current = psu.read_output_current(channel)
                state = psu.read_enabled_state(channel)
                self.msg_queue.put((
                    "update_display",
                    ecu_name,
                    f"当前：{voltage:.2f} V",
                    f"当前：{current:.2f} A",
                    f"状态：{state}"
                ))
            except Exception as e:
                self.msg_queue.put(("error", f"{ecu_name} 数据读取失败：{str(e)}"))
        if not auto:
            self.msg_queue.put(("info", f"正在读取{ecu_name}数据..."))
        threading.Thread(target=worker, daemon=True).start()

    def update_ui_from_queue(self):
        """更新UI（主线程）"""
        try:
            while True:
                msg = self.msg_queue.get_nowait()
                if msg[0] == "info":
                    messagebox.showinfo("操作提示", msg[1], parent=self.root)
                elif msg[0] == "error":
                    messagebox.showerror("操作错误", msg[1], parent=self.root)
                elif msg[0] == "update_display":
                    ecu_name, voltage_text, current_text, state_text = msg[1], msg[2], msg[3], msg[4]
                    getattr(self, f"{ecu_name}_voltage_display")['text'] = voltage_text
                    getattr(self, f"{ecu_name}_current_display")['text'] = current_text
                    getattr(self, f"{ecu_name}_state_display")['text'] = state_text
        except queue.Empty:
            pass
        self.root.after(100, self.update_ui_from_queue)

    def on_closing(self):
        """关闭窗口清理资源"""
        for psu in self.psu_instances.values():
            psu.close()
        self.root.destroy()
        logging.info("程序正常退出，所有串口已关闭")

if __name__ == '__main__':
    root = tk.Tk()
    root.option_add("*Font", "SimHei 9")  # 解决中文显示
    app = ECUControllerUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()