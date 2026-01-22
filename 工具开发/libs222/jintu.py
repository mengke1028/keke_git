import psutil
import requests
import ctypes
import wmi
import hashlib
import uuid
import os

# 初始化WMI对象（复用你原有逻辑）
wmi_obj = wmi.WMI()


# -------------------------- 新增/优化的硬件信息采集函数 --------------------------
def get_physical_mac():
    """获取物理/虚拟网卡的唯一MAC（过滤回环/蓝牙等无效网卡，保留虚拟机网卡）"""
    try:
        for interface, addrs in psutil.net_if_addrs().items():
            # 仅过滤无效虚拟网卡，保留虚拟机业务网卡
            invalid_keywords = ["Loopback", "蓝牙", "VPN", "隧道"]
            if any(keyword in interface for keyword in invalid_keywords):
                continue
            for addr in addrs:
                if addr.family == psutil.AF_LINK and addr.address and addr.address != "00:00:00:00:00:00":
                    return addr.address.replace(":", "").upper()
        # 兜底：系统底层UUID生成MAC（防止无有效网卡）
        return hex(uuid.getnode()).replace("0x", "").zfill(12).upper()
    except Exception as e:
        print(f"获取MAC地址失败: {e}")
        return ""


def get_cpu_serial_number():
    """优化版CPU序列号采集（保留你原有函数名，增强空值处理）"""
    try:
        for processor in wmi_obj.Win32_Processor():
            serial = processor.ProcessorId.strip() if processor.ProcessorId else ""
            return serial
    except Exception as e:
        print(f"获取CPU序列号时出错: {e}")
        return ""


def get_motherboard_serial():
    """新增：获取主板序列号（提升唯一性）"""
    try:
        for board in wmi_obj.Win32_BaseBoard():
            serial = board.SerialNumber.strip() if board.SerialNumber else ""
            return serial
    except Exception as e:
        print(f"获取主板序列号失败: {e}")
        return ""


def get_main_disk_serial():
    """新增：获取系统盘（C盘）序列号（提升唯一性）"""
    try:
        for disk in wmi_obj.Win32_LogicalDisk(DriveType=3):
            if disk.DeviceID == "C:":
                for partition in wmi_obj.Win32_DiskPartition(DriveLetter=disk.DeviceID):
                    for disk_drive in wmi_obj.Win32_DiskDrive(DeviceID=f"\\\\.\\PHYSICALDRIVE{partition.DiskIndex}"):
                        serial = disk_drive.SerialNumber.strip() if disk_drive.SerialNumber else ""
                        return serial
        return ""
    except Exception as e:
        return ""


def get_virtual_machine_identifier():
    """新增：获取虚拟机特有标识（彻底区分克隆虚拟机）"""
    vm_id = ""
    try:
        # 第一步：检测是否为虚拟机环境
        def is_vm():
            for sys in wmi_obj.Win32_ComputerSystem():
                manu = sys.Manufacturer.lower()
                model = sys.Model.lower()
                if "vmware" in manu or "virtual" in model or "hyper-v" in manu or "oracle" in manu:
                    return True
            return False

        if not is_vm():
            return ""  # 物理机返回空，不影响原有逻辑

        # 第二步：适配主流虚拟化平台获取唯一标识
        # VMware
        if os.path.exists("C:\\Program Files\\VMware\\VMware Tools\\vmtoolsd.exe"):
            import subprocess
            result = subprocess.check_output(
                ['vmtoolsd', '--cmd', 'info-get guestinfo.uuid'],
                encoding='utf-8', errors='ignore'
            )
            vm_id = result.strip()
        # VirtualBox
        elif os.path.exists("C:\\Program Files\\Oracle\\VirtualBox Guest Additions\\VBoxControl.exe"):
            import subprocess
            result = subprocess.check_output(
                ['VBoxControl', 'guestproperty', 'get', '/VirtualBox/GuestInfo/UUID'],
                encoding='utf-8', errors='ignore'
            )
            vm_id = result.split()[-1].strip() if result else ""
        # Hyper-V
        else:
            for vm in wmi_obj.Win32_VirtualSystemSettingData():
                if vm.VirtualSystemType == "Microsoft:Hyper-V:System:Realized":
                    vm_id = vm.InstanceID.strip()
                    break

        # 兜底：生成基于系统盘+随机UUID的虚拟机标识
        if not vm_id:
            boot_disk = wmi_obj.Win32_LogicalDisk(DriveType=3, DeviceID="C:")[0]
            vm_id = f"VM_{boot_disk.VolumeSerialNumber}_{uuid.uuid4()}"

    except Exception as e:
        print(f"获取虚拟机标识失败: {e}")
        vm_id = f"VM_FALLBACK_{uuid.uuid4()}"

    return vm_id


def generate_unique_device_id():
    """核心替换：生成唯一设备ID（替代原get_mac函数）"""
    # 1. 采集多维度硬件信息（空值自动过滤）
    hardware_info = [
        get_physical_mac(),
        get_cpu_serial_number(),
        get_motherboard_serial(),
        get_main_disk_serial(),
        str(uuid.getnode())  # 系统底层UUID（克隆虚拟机自动变化）
    ]
    # 2. 补充虚拟机特有标识（关键：区分克隆虚拟机）
    vm_id = get_virtual_machine_identifier()
    if vm_id:
        hardware_info.append(vm_id)

    # 3. 过滤空值并拼接原始字符串
    raw_str = "|".join([info for info in hardware_info if info])
    if not raw_str:  # 极端兜底：所有硬件信息获取失败
        raw_str = str(uuid.uuid4())

    # 4. SHA256哈希生成固定长度的唯一ID（64位，不可逆）
    device_id = hashlib.sha256(raw_str.encode("utf-8")).hexdigest()
    return device_id


# -------------------------- 保留你原有逻辑，仅替换设备ID获取方式 --------------------------
def get_IP():
    """保留你原有IP获取函数（无修改）"""
    try:
        network_adapters = psutil.net_if_addrs()
        for adapter_name, adapter_addresses in network_adapters.items():
            for address in adapter_addresses:
                if str(address.family) == 'AddressFamily.AF_INET':
                    return address.address
        print("无法找到有效的IP地址")
        return None
    except Exception as e:
        print(f"Error getting IP address: {e}")
        return None


# 替换原get_mac函数为新的设备ID生成函数（保持函数名兼容）
get_mac = generate_unique_device_id


def xyg():
    """保留原有逻辑，仅底层设备ID生成方式优化"""
    try:
        url = "https://pwdcheack.oss-cn-beijing.aliyuncs.com/pwd.json"
        res = requests.get(url, timeout=5).text  # 新增超时：防止卡死
        if generate_unique_device_id() not in res:
            return False
        return True  # 新增：授权通过返回True
    except Exception as e:
        print(f"xyg授权检查失败: {e}")
        return False


def daili1():
    """保留原有逻辑，仅底层设备ID生成方式优化"""
    try:
        url = "https://leve1.oss-cn-beijing.aliyuncs.com/pwd.json"
        res = requests.get(url, timeout=5).text  # 新增超时：防止卡死
        if generate_unique_device_id() not in res:
            return False
        return True  # 新增：授权通过返回True
    except Exception as e:
        print(f"daili1授权检查失败: {e}")
        return False


# -------------------------- 主函数（仅少量优化，保持原有逻辑） --------------------------
if __name__ == '__main__':
    # 生成并打印唯一设备ID（用于你登记授权）
    device_id = generate_unique_device_id()
    print(f"当前设备唯一授权ID: {device_id}")

    # 检查授权（优化判断逻辑，更健壮）
    xyg_auth = xyg()
    daili1_auth = daili1()

    if not xyg_auth and not daili1_auth:
        res = ctypes.windll.user32.MessageBoxW(0, "此电脑可能未登记，点击确定开始试用", "授权验证", 1)
        print(f"弹窗返回值: {res}")
        exit()
    else:
        print("设备已授权，程序正常运行")