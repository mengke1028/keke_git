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
    "cookie": 'lianjia_uuid=e52223fe-18af-4b0f-bcc1-695078d15038; ftkrc_=d43cf478-05ba-42f8-9488-e3b40f9562f6; lfrc_=74adbdd7-55a5-408d-bf02-81b2a04a0d86; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22195e9cf386ca5a-0a662cde17e5b3-26011d51-1296000-195e9cf386d2153%22%2C%22%24device_id%22%3A%22195e9cf386ca5a-0a662cde17e5b3-26011d51-1296000-195e9cf386d2153%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E4%BB%98%E8%B4%B9%E5%B9%BF%E5%91%8A%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Fother.php%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E8%B4%9D%E5%A3%B3%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wysuzhou%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; select_city=320500; Hm_lvt_b160d5571570fd63c347b9d4ab5ca610=1745203174,1745825448,1746491890; HMACCOUNT=D626EA63E6B9D7B5; login_ucid=2000000144757586; lianjia_token=2.0011488c957073322b00e5a5a4eaceda71; lianjia_token_secure=2.0011488c957073322b00e5a5a4eaceda71; security_ticket=rxTMEnIIt7dPTu9gGmK+74jsiuCRnjmQjODcVXsw7fft/lYmkhEbtWzl1lfFnnJYW6UtpRdp5GLXHPbPDb/0XB7qT5KVCv7sQ3uXVUrazSGChJLDK58clXGs8tShnY5vSrujDjXcFuPHY8AXoTk4qfOfVi8ybYgRM/tCa7UUbH4=; lianjia_ssid=f07e1d15-6d59-4ffd-bbd7-0e829a56c9b8; Hm_lpvt_b160d5571570fd63c347b9d4ab5ca610=1746491945; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiMDQ5NWI0YTZmMTdkMzkyZjVkNWQwZWVkMjY1NTQ2MGQzOTdjMzkyYWQ1NDc4NTM3NWQwNGE4OTY5NzAwMjQyMTVkZjkxZWI1MDFjN2JlYTE0ZDRkMmI2Y2NhZWFiMzRmNTNhMGRjNGE4Y2QwMGNkNjA5YzVhOTJhNjY0Y2QxMWZlYjc4NDliNjg5MjJiNjM0YjllNTU4YjFlM2FmMjA0MWM5NGQ5YTY3N2MzZDA5NGI0NjRmNzIxNjk4ZWIwNTdjZGE1NTFhMTM4MTdmNDE5NmYyNzY1NTgxYzI3MWI5ZjEwZmVmYjIyOTljNDM0MzY2NDk0OTE4ZWM0OTZjYjNkOVwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCIxNzc5MzA3MFwifSIsInIiOiJodHRwczovL3N1LmtlLmNvbS8/dXRtX3NvdXJjZT1iYWlkdSZ1dG1fbWVkaXVtPXBpbnpodWFuJnV0bV90ZXJtPWJpYW90aSZ1dG1fY29udGVudD1iaWFvdGltaWFvc2h1JnV0bV9jYW1wYWlnbj13eXN1emhvdSIsIm9zIjoid2ViIiwidiI6IjAuMSJ9'
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
        # print(urls)
        res = requests.get(urls, headers=headers)
        # print(res.text)
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
    for xiaoqu in ["金御华府"]:
        datas = get_jiage(xiaoqu)
        save_data(datas, xiaoqu)
