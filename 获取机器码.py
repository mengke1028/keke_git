import platform

# 获取系统版本号
system_version = platform.win32_ver()[1]

if system_version.startswith('6.1'):
    print("当前系统是 Windows 7")
elif system_version.startswith('10.0'):
    print("当前系统是 Windows 10")
else:
    print(f"当前系统不是 Windows 7 或 Windows 10，系统版本号是 {system_version}")