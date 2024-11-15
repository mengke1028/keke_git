import tkinter as tk
from tkinter import scrolledtext
import json
import sys


def headers_to_json(headers_str, separator=": "):
    """
    将给定的HTTP头部字符串转换为JSON对象。

    :param headers_str: 包含多个HTTP头的字符串，每行一个头。
    :param separator: 用于分割每个头中的键和值，默认为": "。
    :return: JSON格式的字符串表示。
    """
    # 初始化字典来存储结果
    headers_dict = {}

    # 按行分割输入字符串
    lines = headers_str.strip().split("\n")
    for line in lines:
        if line:  # 过虑空行
            # 使用指定分隔符分割每一行
            key, value = line.replace('"', '\'').split(separator, 1)
            headers_dict[key] = value.strip()  # 移除可能存在的多余空白

    # 转换成JSON字符串
    return json.dumps(headers_dict, indent=4)


def log_message(log_text, message):
    """ 向指定的日志框添加消息 """
    log_text.insert(tk.END, message)
    log_text.see(tk.END)  # 滚动到底部


def clear_log(log_text):
    """ 清除指定的日志框内容 """
    log_text.delete(1.0, tk.END)


def on_log_button_click():
    """ 当点击日志按钮时调用此函数 """
    test = log_text_1.get('1.0', tk.END)
    jsons = headers_to_json(test)

    print(jsons)
    # log_message(log_text_1, "这是第一个日志框的消息")
    log_message(log_text_2, str(jsons))
    log_text_1.delete(1.0, tk.END)


# 创建主窗口
root = tk.Tk()
root.title("双日志输出框示例")
root.geometry("800x400")

# 创建第一个日志框
log_frame_1 = tk.Frame(root)
log_frame_1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

log_label_1 = tk.Label(log_frame_1, text="请求头")
log_label_1.pack()

log_text_1 = scrolledtext.ScrolledText(log_frame_1, wrap=tk.WORD, height=15, width=40)
log_text_1.pack(fill=tk.BOTH, expand=True)

# 创建第二个日志框
log_frame_2 = tk.Frame(root)
log_frame_2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

log_label_2 = tk.Label(log_frame_2, text="JSON格式")
log_label_2.pack()

log_text_2 = scrolledtext.ScrolledText(log_frame_2, wrap=tk.WORD, height=15, width=40)
log_text_2.pack(fill=tk.BOTH, expand=True)

# 创建一个按钮来生成日志
log_button = tk.Button(root, text="转换成json", command=on_log_button_click)
log_button.pack(pady=10)

# 启动事件循环
root.mainloop()
