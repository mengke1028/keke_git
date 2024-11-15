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


# 示例使用
if __name__ == "__main__":
    # 示例HTTP头部
    sample_headers = """Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: max-age=0
Connection: keep-alive
Cookie: BIDUPSID=7A6A799D8E1EDF433061DF594F5C2C31; PSTM=1729822026; BAIDUID=7A6A799D8E1EDF433AE9A75546AA184D:FG=1; BAIDUID_BFESS=7A6A799D8E1EDF433AE9A75546AA184D:FG=1; BD_UPN=12314753; ZFY=Um4BC0K8KJjE1NNPxezL6BO21SqUZRVHPo8vAy95CVM:C; MCITY=-224%3A; Hm_lvt_9f14aaa038bbba8b12ec2a4a3e51d254=1730182291; B64_BOT=1; COOKIE_SESSION=8272_0_1_2_1_1_1_0_1_1_0_0_0_0_7_0_1730190589_0_1730190596%7C2%230_0_1730190596%7C1; H_PS_PSSID=60977_61027_61022; BD_HOME=1; BA_HECTOR=ag8l05802k8k2h8l2k048h0g32qud11ji88r31u
Host: www.baidu.com
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36
sec-ch-ua: "Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: 'Windows'"""

    # 调用函数并打印结果
    print(headers_to_json(sample_headers))
