import random
import string

# 定义激活码长度和生成数量
code_length = 20
code_count = 30

# 定义字符集
characters = string.ascii_letters + string.digits

# 打开文件以写入激活码
try:
    with open('activation_codes.txt', 'w') as file:
        # 生成激活码
        for _ in range(code_count):
            activation_code = ''.join(random.choice(characters) for _ in range(code_length))
            file.write(activation_code + '\n')
    print("激活码已成功保存到 activation_codes.txt 文件中。")
except Exception as e:
    print(f"保存文件时出现错误: {e}")
