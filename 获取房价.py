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
    "cookie": 'lianjia_uuid=1084109d-1d16-4f84-9418-0fc95c1a57a0; crosSdkDT2019DeviceId=6pjv6h--5dfoxp-iqoq8ajdo1u3kgn-oemyj38fh; ftkrc_=3ea494b2-74e3-4a5f-b5d6-acdebad2f4fc; lfrc_=627651a6-3edf-4303-907d-809e6ee42551; select_city=320500; Hm_lvt_b160d5571570fd63c347b9d4ab5ca610=1771998272; HMACCOUNT=42DAF29B51BAE917; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219a9aeafbc4cc-025da860ad75248-26061851-1296000-19a9aeafbc5ac%22%2C%22%24device_id%22%3A%2219a9aeafbc4cc-025da860ad75248-26061851-1296000-19a9aeafbc5ac%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E4%BB%98%E8%B4%B9%E5%B9%BF%E5%91%8A%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Fother.php%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E8%B4%9D%E5%A3%B3%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wysuzhou%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; login_ucid=2000000144757586; lianjia_token=2.00105b73037160cdbd01f65a32e89eb791; lianjia_token_secure=2.00105b73037160cdbd01f65a32e89eb791; security_ticket=Xlg6oJfN7vMRGE29tp1wE2pr3mkAgpbXwXtKVseQxH7EBeC8b1fOUch278UKUV4qYhrfLcaLwiHEtrYrGtz74RPxvAqKk8+13e5B336SdY4kt+kg/o2Vh6PMPVtJFWrgm3oL+donFXNenVy4MOQHaQmHwq10pd9Vybob8k34TAs=; Hm_lpvt_b160d5571570fd63c347b9d4ab5ca610=1771998294; lianjia_ssid=db81279f-7b6e-4757-aad7-5989f53eb92b'
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
