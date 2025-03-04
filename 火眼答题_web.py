import requests

url = 'http://dt1.hyocr.com:8080/uploadpic.php'

import time



file_path = '1.jpg'
data = {
    'dati_type': 8016,
    'acc_str': 'gVpvbTKYcrz1PDHw',
    # 'extra_str': '',
    # 'zz': '',
    'pri': 1,
    'timeout': 60,
}

"""读取图片文件并返回字节数组"""
with open(file_path, 'rb') as file:
    files = {'pic': file}
    res = requests.post(url=url, data=data, files=files)
    res.encoding = 'GBK'
    print(res.text)
while True:

    if '#' not in res.text:
        get_url = f'http://dt1.hyocr.com:8080/query.php?sid={res.text}'
        res_get = requests.get(get_url)
        print(res_get.text)
        if res_get.text != '':
            break
    time.sleep(1)