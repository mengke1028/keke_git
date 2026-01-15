# -*- coding: utf-8 -*-
# Keke.Meng  2025/4/2 8:40
from datetime import datetime

import requests
import time
import ast

"""
手动查看 https://quote.cngold.org/gjs/swhj_zghj.html
"""


class Mai:
    def jinjia(self, data):
        time_tag = int(time.time() * 1000)

        url = 'https://api.jijinhao.com/quoteCenter/realTime.htm?codes=JO_52683,JO_52684,JO_52685,&_={}'.format(
            time_tag)
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9",
            "referer": "https://quote.cngold.org/gjs/swhj_zghj.html",
            "sec-ch-ua": "'Google Chrome';v='131', 'Chromium';v='131', 'Not_A Brand';v='24'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "'Windows'",
            "sec-fetch-dest": "script",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "cross-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }

        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        # print(res.text)
        datas = (res.text[30:])
        JO_52683 = None
        datas_json = ast.literal_eval(str("{" + datas))  # 字符串形式的json 直接转成json
        for jo in ['JO_52683', 'JO_52684', 'JO_52685']:
            if jo == 'JO_52683':
                JO_52683 = datas_json[jo]['q2']
            jichu = datas_json[jo]['q2']
            print(datas_json[jo]['showName'], jichu)
        return JO_52683


if __name__ == '__main__':
    current_time = datetime.now().strftime("%Y-%m-%d")
    print(current_time)
    M = Mai()
    M.jinjia(0)

"""


2025-10-16
中国黄金基础金价 954.0
投资金条/储值金条/元宝金：零售价 970.0
投资金条/储值金条/元宝金：回购价 951.0


"""
