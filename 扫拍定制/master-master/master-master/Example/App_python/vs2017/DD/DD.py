import time

try:
    # 以读取模式打开文件
    with open('xinxi.txt', 'r', encoding='utf-8') as fp:
        # 读取文件的所有内容
        content = fp.readlines()
        content = [line.strip() for line in content]
        print(content)
except FileNotFoundError:
    print("指定的文件未找到，将创建新文件。")
# 如果文件不存在或者 data 不在文件中，将 data 写入文件

