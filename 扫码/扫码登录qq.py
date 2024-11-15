import requests
import time
import re
from PIL import Image
from io import BytesIO

qr_code_image = None


def Get_bkn(pSkey):
    # 计算bkn
    t, n, o = 5381, 0, len(pSkey)
    while n < o:
        t += (t << 5) + ord(pSkey[n])
        n += 1
    return t & 2147483647


def Get_ptqrToken(qrsig):
    # 计算ptqrtoken
    n, i, e = len(qrsig), 0, 0
    while n > i:
        e += (e << 5) + ord(qrsig[i])
        i += 1
    return 2147483647 & e


def Get_QRcode():
    # 获取 腾讯网 二维码
    global qr_code_image
    url = 'https://ssl.ptlogin2.qq.com/ptqrshow?appid=549000912&e=2&l=M&s=3&d=72&v=4&t=0.8692955245720428&daid=5&pt_3rd_aid=0'

    try:
        r = requests.get(url)
        qrsig = requests.utils.dict_from_cookiejar(r.cookies).get('qrsig')

        qr_code_image = Image.open(BytesIO(r.content))
        qr_code_image.show()
        print(time.strftime('%H:%M:%S'), ' 登录二维码获取成功')
        return qrsig
    except Exception as e:
        print(time.strftime('%H:%M:%S') + " 获取二维码报错" + str(e))
        print('第' + str(e.__traceback__.tb_lineno) + '行文件报错')


def Get_QQ():
    global qq_number, qr_code_image
    # 获取cookie
    qrsig = Get_QRcode()
    print(qrsig)
    ptqrtoken = Get_ptqrToken(qrsig)
    while True:
        url = 'https://ssl.ptlogin2.qq.com/ptqrlogin?u1=https%3A%2F%2Fqzs.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&ptqrtoken=' + str(
            ptqrtoken) + '&ptredirect=0&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0-' + str(
            time.time()) + '&js_ver=20032614&js_type=1&login_sig=&pt_uistyle=40&aid=549000912&daid=5&'
        cookies = {'qrsig': qrsig}
        try:
            session = requests.session()
            r = session.get(url, cookies=cookies)
            print(r.text)
            if '二维码未失效' in r.text:
                print(time.strftime('%H:%M:%S'), ' 二维码未失效')
            elif '二维码认证中' in r.text:
                print(time.strftime('%H:%M:%S'), ' 二维码认证中')
            elif '二维码已失效' in r.text:
                print(time.strftime('%H:%M:%S'), ' 二维码已失效')
                qrsig = Get_QRcode()
                ptqrtoken = Get_ptqrToken(qrsig)
            elif '登录成功' in r.text:
                print(time.strftime('%H:%M:%S'), ' 登录成功')
                qq_number = re.findall(r'&uin=(.+?)&service', r.text)[0]
                return qq_number, session
        except Exception as e:
            print(time.strftime('%H:%M:%S') + " 获取cookie报错" + str(e))
            print('第' + str(e.__traceback__.tb_lineno) + '行文件报错')
        time.sleep(2)


if __name__ == '__main__':
    qq, session = Get_QQ()
    print(session)
    res = session.get("https://user.qzone.qq.com/")
    res.encoding = "utf-8"
    with open("qq空间.html",'w',encoding='utf-8') as fp:
        fp.write(res.text)
