import json
import requests

# 读取保存的 Cookie 文件
with open(r'cf_cookie.json', 'r') as f:
    cookie_list = json.load(f)

# 提取 name 和 value 并构建 requests 可用的 Cookie 字典
cookies = {cookie['name']: cookie['value'] for cookie in cookie_list}

# 打印 Cookie 以供检查
print(cookies)

# 使用提取的 Cookie 发送请求
url = "https://cf.qq.com/"
response = requests.get(url, cookies=cookies)

# 检查响应状态码和内容
if response.status_code == 200:
    print("请求成功")
    # 打印响应内容
    response.encoding="GBK"
    print(response.text)
else:
    print(f"请求失败，状态码: {response.status_code}")
