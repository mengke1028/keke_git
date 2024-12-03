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
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
accept-encoding:
gzip, deflate, br, zstd
accept-language:
zh-CN,zh;q=0.9
cache-control:
max-age=0
cookie:
pgv_pvid=1192823866; fqm_pvqid=a15878de-9bd0-4c3d-95c8-f580ba1da18d; fqm_sessionid=04d82731-50dc-4973-8abe-95a20d8d5bd7; pgv_info=ssid=s1822598732; ts_last=y.qq.com/; ts_uid=7137318850; _qpsvr_localtk=0.7158129546864633; euin=oK6kowEAoK4z7eSq7wcq7K657n**; wxunionid=oqFLxsnY48Wwdtir8x575k70CRmc; tmeLoginType=1; qm_keyst=W_X_63B0aAr5861YPzppUhAAde77XVfEl2iFyWv5C7IaU8skWt1RIBpf7gDKaH-9HLfYFlwvq5xOWMpoYk1uIMdKzITujgSA; qqmusic_key=W_X_63B0aAr5861YPzppUhAAde77XVfEl2iFyWv5C7IaU8skWt1RIBpf7gDKaH-9HLfYFlwvq5xOWMpoYk1uIMdKzITujgSA; psrf_qqunionid=; wxuin=1152921504796895114; psrf_qqaccess_token=; wxrefresh_token=86_4s3Z_mM6xl2E7j0B5BgRmZcHZ9U8jLb0IToVtAJm7GM21dVRXjm7ROTa4Bu7kgBgMrXgoqlLrua6tyjS-aRJgenfRuYO7YB7m-5GwlRaX7Y; psrf_qqopenid=; psrf_qqrefresh_token=; qm_keyst=W_X_63B0aAr5861YPzppUhAAde77XVfEl2iFyWv5C7IaU8skWt1RIBpf7gDKaH-9HLfYFlwvq5xOWMpoYk1uIMdKzITujgSA; wxopenid=opCFJw6ZXEkg1mt0HtKJ-lMBcscs; wxuin=1152921504796895114; login_type=2
priority:
u=0, i
referer:
https://y.qq.com/portal/wx_redirect.html?login_type=2&surl=https%3A%2F%2Fy.qq.com%2F&code=071lE7Ha1FVfCI0KjoGa19dH7Q2lE7H6&state=STATE
sec-ch-ua:
"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"
sec-ch-ua-mobile:
?0
sec-ch-ua-platform:
"Windows"
sec-fetch-dest:
document
sec-fetch-mode:
navigate
sec-fetch-site:
same-origin
sec-fetch-user:
?1
upgrade-insecure-requests:
1
user-agent:
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36
"""

    # 调用函数并打印结果
    print(headers_to_json(sample_headers))
