import ctypes
import time

# 使用 WinDLL 加载动态链接库，确保调用约定正确
hydati_dll = ctypes.WinDLL(r'D:\keke\HYDati.dll')

# 定义函数原型
# SendImage 函数
SendImage = hydati_dll.SendImage
SendImage.argtypes = [
    ctypes.c_char_p,  # 参数1 字符型，验证密码串
    ctypes.c_int,  # 参数2 整数型，截图坐标X
    ctypes.c_int,  # 参数3 整数型，截图坐标y
    ctypes.c_int,  # 参数4 整数型，截图宽度
    ctypes.c_int,  # 参数5 整数型，截图高度
    ctypes.c_int,  # 参数6 整数型，题目类型ID(游戏ID)
    ctypes.c_int,  # 参数7 整数型, 题目最大允许时间
    ctypes.c_int,  # 参数8 整数型, 固定1
    ctypes.c_char_p  # 参数9 字符型, 备注（题目文本说明)
]
SendImage.restype = ctypes.c_void_p
SendImage.restype = ctypes.c_void_p

# GetAnswer 函数
GetAnswer = hydati_dll.GetAnswer
GetAnswer.argtypes = [ctypes.c_char_p]
GetAnswer.restype = ctypes.c_void_p


def read_image_file(file_path):
    """读取图片文件并返回字节数组"""
    with open(file_path, 'rb') as file:
        image_data = file.read()
    return image_data


def convert_to_byte_array(data):
    """将字节数据转换为 ctypes 字节数组"""
    byte_array = (ctypes.c_byte * len(data))()
    for i in range(len(data)):
        byte_array[i] = data[i]
    return byte_array


def call_send_image(auth_code, x, y, width, height, question_type_id, max_time, remark):
    """调用 SendImage 函数"""
    auth_code_bytes = auth_code.encode('ascii')
    remark_bytes = remark.encode('ascii')
    tid_ptr = SendImage(auth_code_bytes, x, y, width, height, question_type_id, max_time, 1, remark_bytes)
    tid = ctypes.string_at(tid_ptr).decode('ascii')
    return tid


def call_get_answer(tid):
    """调用 GetAnswer 函数"""
    tid_bytes = tid.encode('ascii')
    answer_ptr = GetAnswer(tid_bytes)
    answer = ctypes.string_at(answer_ptr).decode('ascii')
    return answer


def main():
    file_path = '12.jpg'
    x = 10
    y = 20
    width = 500
    height = 500
    auth_code = 'gVpvbTKYcrz1PDHw'
    question_type = 8016
    timeout = 60
    pri = 1
    remark = ''

    # 读取图片文件
    image_data = read_image_file(file_path)
    data_length = len(image_data)

    # 调用 SendImage 函数
    tid = call_send_image(auth_code, x, y, width, height, question_type, timeout, remark)
    print(tid)
    # 循环调用 GetAnswer 函数，直到获取到结果或超时
    for i in range(timeout):
        answer = call_get_answer(tid)
        if answer:
            print(f"识别结果: {answer}")
            break
        time.sleep(1)
    else:
        print("超时未获取到识别结果")


if __name__ == "__main__":
    time.sleep(2)
    main()
