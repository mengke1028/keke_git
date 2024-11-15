import requests
import json
import base64
import hmac
import hashlib
import time

# 电脑端钉钉群里添加自定义机器人获取,第一步的“Webhook”链接后缀
access_token = '6c5bef0cba35b7790bbc9a346acbad0257e5a50aea9db82e56338df76a66e53e'
# 从钉钉机器人设置中获取，即第一步的“加签”
secret = 'SEC843710383730d574ae39a4811157d337d1420afc9d1f8ccfb0d4641187937d3f'
# 发送HTTP GET请求

# 当前时间戳
timestamp = str(round(time.time() * 1000))

# 拼接字符串
string_to_sign = '{}\n{}'.format(timestamp, secret)

# 生成签名
sign = hmac.new(secret.encode('utf-8'), string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()
sign = base64.b64encode(sign).decode('utf-8')

webhook_url = 'https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}'.format(access_token,
                                                                                                 timestamp, sign)

msg = {
    'msgtype': 'text',
    'text': {
        'content': ' 要发送的文字'
    }
}
# 发送POST请求
response = requests.post(webhook_url, data=json.dumps(msg), headers={'Content-Type': 'application/json'})

# 所有返回的内容
print(response.json())

# 打印响应状态码
print(response.status_code)

# 打印响应内容
print(response.text)
