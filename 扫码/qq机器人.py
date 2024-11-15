import requests
from PIL import Image
from io import BytesIO
import time


# 获取二维码的 URL 和 ticket
def get_qr_code():
    url = 'https://ssl.ptlogin2.qq.com/ptqrshow?appid=549000912&e=2&l=M&s=5&d=72&v=4&t=0.5'
    response = requests.get(url)
    if response.status_code == 200:
        return response.content, url
    else:
        raise Exception(f"请求失败，状态码: {response.status_code}")


# 显示二维码AA
def show_qr_code(qr_code_content):
    qr_code_image = Image.open(BytesIO(qr_code_content))
    qr_code_image.show()


# 轮询二维码状态
def poll_qr_status(ticket):
    print("token=",ticket)
    check_url = f'https://ssl.ptlogin2.qq.com/ptqrlogin?u1=https%3A%2F%2Fqzone.qq.com%2F&ptqrtoken={ticket}&ptredirect=0&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0-1586073493777&js_ver=10286&js_type=1&login_sig=&pt_uistyle=40&aid=549000912&daid=5&'
    while True:
        print(check_url)
        response = requests.get(check_url)
        print(response)
        if "二维码未失效" in response.text:
            print("等待扫码...")
        elif "二维码认证中" in response.text:
            print("正在认证...")
        elif "登录成功" in response.text:
            print("登录成功")
            # 解析响应中的 cookies
            cookies = response.cookies
            return cookies
        else:
            print("登录失败，请重试")
            return None
        time.sleep(2)  # 每隔2秒轮询一次


# 主函数
def main():
    try:
        # 获取二维码
        qr_code_content, qr_code_url = get_qr_code()

        # 显示二维码
        show_qr_code(qr_code_content)

        # 提取 ticket
        ticket = qr_code_url.split('&')[4].split('=')[1]

        # 轮询二维码状态
        session_cookies = poll_qr_status(ticket)

        if session_cookies:
            print("Session Cookies:", session_cookies)
        else:
            print("登录失败，请重试")
    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":

    main()
