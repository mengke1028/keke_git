import hid
import time

# ===================== 核心配置（必须替换为你的设备参数） =====================
CH9329_VID = 0x1A86          # 你的CH9329 VID
CH9329_PID = 0xDE29          # 你的CH9329 PID
MOUSE_REPORT_ID = 0x02       # 鼠标报告ID（复合设备模式下默认0x02，无效试0x01/0x03）
MOUSE_MAX_STEP = 127         # 单次最大偏移（CH9329限制-128~127）
# ============================================================================

# USB HID鼠标协议常量
MOUSE_BTN_NONE = 0x00        # 无按键
MOUSE_BTN_LEFT = 0x01        # 左键
MOUSE_BTN_RIGHT = 0x02       # 右键
MOUSE_BTN_MIDDLE = 0x04      # 中键

class CH9329HIDMouse:
    def __init__(self, vid, pid, mouse_report_id):
        self.vid = vid
        self.pid = pid
        self.mouse_report_id = mouse_report_id
        self.device = None
        self.open_device()

    def open_device(self):
        """打开CH9329的HID设备（仅鼠标通道）"""
        # 步骤1：枚举设备找到目标路径
        target_path = None
        for dev in hid.enumerate():
            if dev['vendor_id'] == self.vid and dev['product_id'] == self.pid:
                target_path = dev['path']
                print(f"🔹 找到CH9329设备：{dev['product_string']} (路径：{target_path})")
                break

        if not target_path:
            raise Exception("❌ 未找到CH9329设备，请检查VID/PID或设备连接")

        # 步骤2：打开设备并设置非阻塞模式
        self.device = hid.device()
        self.device.open_path(target_path)
        self.device.set_nonblocking(1)
        print("✅ CH9329 HID设备打开成功（仅鼠标控制）")

    def close_device(self):
        """关闭HID设备"""
        if self.device:
            self.device.close()
            print("🔹 CH9329 HID设备已关闭")

    def _convert_to_8bit(self, value):
        """将偏移量转换为8位补码（适配CH9329的-128~127范围）"""
        if value > 127:
            return 127
        elif value < -128:
            return -128
        # 转换为无符号8位字节（负数自动转补码）
        return value & 0xFF

    def send_mouse_packet(self, buttons, dx, dy, wheel=0x00):
        """
        发送原始鼠标HID数据包（核心方法）
        :param buttons: 鼠标按键掩码（MOUSE_BTN_*）
        :param dx: X轴偏移（左移为负，右移为正）
        :param dy: Y轴偏移（上移为负，下移为正）
        :param wheel: 滚轮偏移（上滚为正，下滚为负）
        """
        # 转换偏移量为8位补码
        dx_8bit = self._convert_to_8bit(dx)
        dy_8bit = self._convert_to_8bit(dy)
        wheel_8bit = self._convert_to_8bit(wheel)

        # 构造鼠标数据包（复合设备模式标准格式：报告ID+4字节数据）
        mouse_packet = [
            self.mouse_report_id,  # 鼠标报告ID（关键）
            buttons,               # 按键掩码
            dx_8bit,               # X偏移
            dy_8bit,               # Y偏移
            wheel_8bit             # 滚轮偏移
        ]

        # 发送数据包到CH9329
        self.device.write(bytes(mouse_packet))
        # 短延时确保指令被CH9329接收（不可省略）
        time.sleep(0.02)

    def move_to_top_left(self, max_attempts=30):
        """
        纯HID协议将鼠标移到左上角（通过连续发送左/上偏移）
        :param max_attempts: 最大尝试次数（确保超出屏幕边界）
        """
        print("\n🔹 开始通过HID协议移动鼠标到左上角...")
        attempts = 0

        # 连续发送最大左/上偏移，直到尝试次数用尽（屏幕左上角是边界，多次发送必到）
        while attempts < max_attempts:
            # 发送单次最大左移（-127）+ 最大上移（-127）
            self.send_mouse_packet(MOUSE_BTN_NONE, -MOUSE_MAX_STEP, -MOUSE_MAX_STEP)
            attempts += 1
            # 每5次打印进度
            if attempts % 5 == 0:
                print(f"   已发送{attempts}次左/上偏移指令")

        print(f"✅ 鼠标移到左上角完成（共发送{attempts}次指令）")

    def right_click(self, press_delay=0.2):
        """
        纯HID协议实现鼠标右键单击
        :param press_delay: 右键按下时长（确保系统识别）
        """
        print("\n🔹 开始通过HID协议执行右键单击...")
        # 步骤1：按下右键
        self.send_mouse_packet(MOUSE_BTN_RIGHT, 0, 0)
        time.sleep(press_delay)
        # 步骤2：释放右键
        self.send_mouse_packet(MOUSE_BTN_NONE, 0, 0)
        print("✅ 右键单击完成")

    def right_double_click(self, press_delay=0.1, interval=0.1):
        """纯HID协议实现右键双击"""
        print("\n🔹 开始通过HID协议执行右键双击...")
        # 第一次单击
        self.send_mouse_packet(MOUSE_BTN_RIGHT, 0, 0)
        time.sleep(press_delay)
        self.send_mouse_packet(MOUSE_BTN_NONE, 0, 0)
        time.sleep(interval)
        # 第二次单击
        self.send_mouse_packet(MOUSE_BTN_RIGHT, 0, 0)
        time.sleep(press_delay)
        self.send_mouse_packet(MOUSE_BTN_NONE, 0, 0)
        print("✅ 右键双击完成")

# ===================== 测试主逻辑（纯HID，无pyautogui） =====================
if __name__ == "__main__":
    try:
        # 初始化CH9329 HID鼠标控制器
        mouse_ctrl = CH9329HIDMouse(
            vid=CH9329_VID,
            pid=CH9329_PID,
            mouse_report_id=MOUSE_REPORT_ID
        )

        # 步骤1：移到左上角（纯HID指令）
        mouse_ctrl.move_to_top_left(max_attempts=30)

        # 步骤2：右键单击（纯HID指令）
        mouse_ctrl.right_click(press_delay=0.2)

        # 可选：右键双击
        # mouse_ctrl.right_double_click()

    except Exception as e:
        print(f"\n❌ 执行错误：{e}")
    finally:
        # 确保设备关闭
        if 'mouse_ctrl' in locals():
            mouse_ctrl.close_device()