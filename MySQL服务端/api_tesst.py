# -*- coding: utf-8 -*-
# TCN01475  2026/3/6 8:55
import requests

API_URL = "http://127.0.0.1:5000/verify_code"

code = '06DtPKvawZ7b5ckJKETh'
# 发送POST请求到后端API
response = requests.post(
    API_URL,
    json={"code": code},
    timeout=10  # 超时时间10秒
)
response.raise_for_status()  # 检查HTTP请求是否成功
print(response)
result = response.json()
print(result)
