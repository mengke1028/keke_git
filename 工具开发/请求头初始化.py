import json
import sys


def headers_to_json(headers_str, separator=":\n"):
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
    for item, line in enumerate(lines):
        if line[-1] == ':':
            headers_dict[line[:-1]] = lines[int(item)+1].replace('"', "'")
        #
        # if line:  # 过虑空行
        #     # 使用指定分隔符分割每一行
        #     key, value = line.replace('"', '\'').split(separator, 1)
        #     headers_dict[key] = value.strip()  # 移除可能存在的多余空白

    # 转换成JSON字符串
    return json.dumps(headers_dict, indent=4)


# 示例使用
if __name__ == "__main__":
    # 示例HTTP头部
    sample_headers = """
accept:
*/*
accept-encoding:
gzip, deflate, br, zstd
accept-language:
zh-CN,zh;q=0.9
referer:
https://quote.cngold.org/gjs/swhj_zghj.html
sec-ch-ua:
"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"
sec-ch-ua-mobile:
?0
sec-ch-ua-platform:
"Windows"
sec-fetch-dest:
script
sec-fetch-mode:
no-cors
sec-fetch-site:
cross-site
user-agent:
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"""

    # 调用函数并打印结果
    print(headers_to_json(sample_headers))
