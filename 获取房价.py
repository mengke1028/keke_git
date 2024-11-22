import random
import time
import requests
from lxml import etree
import csv


# 随机获得ua
def get_ua():
    first_num = random.randint(55, 62)
    third_num = random.randint(0, 3200)
    fourth_num = random.randint(0, 140)
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
        '(Macintosh; Intel Mac OS X 10_12_6)'
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                  )
    return ua


headers = {
    'user-agent': get_ua(),
    "cookie": 'SECKEY_ABVK=IkTNnbOwlKxY6gZ3/u8wXVJlcQNtA3jFPOKT4BAi2B0%3D; lianjia_uuid=ff3cd500-5269-41cc-9b72-fc940f8da934; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22192dad812e896e-007a5f6cc52397-4c657b58-1296000-192dad812e9225d%22%2C%22%24device_id%22%3A%22192dad812e896e-007a5f6cc52397-4c657b58-1296000-192dad812e9225d%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E4%BB%98%E8%B4%B9%E5%B9%BF%E5%91%8A%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Fother.php%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E8%B4%9D%E5%A3%B3%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wysuzhou%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; ftkrc_=724951c9-bd0f-439c-a549-21b6b839e8a0; lfrc_=eb5f890a-fe69-4ff2-8bbd-b4d5052fe845; select_city=320500; lianjia_ssid=b045f1a2-448a-486d-b07c-c6097a2e5ac2; crosSdkDT2019DeviceId=oegrgs--yidxgw-kzzo3eg2qh6sqrm-mvkfpksma; login_ucid=2000000144757586; lianjia_token=2.0015dbc25374e07ced0476eb62e547a742; lianjia_token_secure=2.0015dbc25374e07ced0476eb62e547a742; security_ticket=L//DoJr9djQZxYPy2SY7MKtEtnJXHj8PiWAN1kEk4rnNicCukH2CmeSFjF1+poBvrmNw8GTNkDjd3EKucE/uj9X3x4E2ga2pNCuhsuQ4K5lZjETKZK8P4grkTQIGLF5AF97sS+gImf+0VwQBrZrPnuM7Y1B9yrykkGcT15ROPhI=; Hm_lvt_b160d5571570fd63c347b9d4ab5ca610=1730422499,1730698281,1730767775,1731055541; HMACCOUNT=93609AFD8F9BA74C; hip=dsmaPaVG4bblouNQBeH3hmoJ-cK1F_W2zQi7jtdGUP91jNrLlvS7bRQq2Ft6A54sp0YtkRD_pgLdpUSuYBzPkLF9Vo2tZs_9t7JqORWhJOwOwE4DXrI3Dl77awugylBfxM6zG8qYTT1zpgbSPYTTa5yC8w5TTcEupUaOIvC7CC9Ac1xDkho%3D; Hm_lpvt_b160d5571570fd63c347b9d4ab5ca610=1731055600; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiY2QxYjA0MTQ5OWU0MWJmYmM2NjczNDEyYjFjYTNkZGJhMTgxMGJjZWI1YmJhYTUwNDEzMDI5MWFkMjhmMGY4N2NjODFmYTY2MzFjMDAyYTRiN2ZjMzBkOTk2MTlmOWU3YmEyN2I4ZTJjMmFjY2FkMWJlMTk3NjU1ZTE2NjllZWQzY2QxODVkMWVjYWViOTJiMjQ4ZWFjNjEwNDkyMGI3NjM5YjRlZWNlODI4YzYwZDFlNjIwZGMwMzI0ZDdkZjY1ZDRlMWIwMGQ5YTQxNTVlMzRhZjQ2NDhlOWQ2M2YxZjI1NTVjMTAyZDk2ODViODQ1MDU5MTVhMWNhZDQwODA5ZVwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI1NDA3N2U1N1wifSIsInIiOiJodHRwczovL3N1LmtlLmNvbS9jaGVuZ2ppYW8vIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0='
}


def get_jiage(xiaoqu):
    datas = []
    if "魅力花园" in xiaoqu:
        lens = 10
        flog = "c239821887922921"
    elif "金御华府" in xiaoqu:
        lens = 4
        flog = "c239821887923015"
    else:
        return
    for u in range(1, lens):
        urls = f'https://su.ke.com/ershoufang/pg{u}{flog}/'
        res = requests.get(urls, headers=headers)
        res.encoding = res.apparent_encoding
        html = etree.HTML(res.text)
        # print(res.text)
        items = html.xpath('//li[@class="clear"]')

        for i in items:
            jiage = i.xpath('./div/div[2]/div[5]/div[1]/span/text()')[0]
            jiage2 = float(jiage.replace(' ', '').replace('\n', ''))
            url = i.xpath("./div/div[1]/a/@href")[0]
            t = i.xpath('./div/div[2]/div[2]/text()')[1]
            t2 = t.replace(' ', '').replace('\n', '')
            if "魅力花园" in xiaoqu:
                if '共9层' in t2:
                    datas1 = (int(jiage2), t2, url)
                    datas.append(datas1)
            elif "金御华府" in xiaoqu:
                if '共18层' in t2:
                    datas1 = (int(jiage2), t2, url)
                    datas.append(datas1)

        time.sleep(2)
    return datas


def save_data(datas, xiaoqu):
    sorted_pairs = sorted(datas, key=lambda pair: pair[0])
    if len(sorted_pairs) == 0:
        print('没有数据')
        return
    file = open('{}.csv'.format(xiaoqu), 'w', newline='', encoding='utf-8')
    for data in sorted_pairs:
        writer = csv.writer(file)
        writer.writerows([data])
    print(f"{xiaoqu}CSV文件保存成功！")


if __name__ == '__main__':
    # xiaoqu = "魅力花园"
    for xiaoqu in ["魅力花园", "金御华府"]:
        datas = get_jiage(xiaoqu)
        save_data(datas, xiaoqu)
