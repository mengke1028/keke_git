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
    "cookie": 'lianjia_uuid=0dbe3e5b-bc25-4f58-83e3-42b55c08927a; ftkrc_=ef68e88b-e429-4818-ba8a-8ff163eaaf49; lfrc_=95bdee9b-d773-45ab-a4f8-db9597827946; crosSdkDT2019DeviceId=u8ko45-vtswrp-h82wsepcrkzt8zm-xk5rm69zg; select_city=320500; Hm_lvt_b160d5571570fd63c347b9d4ab5ca610=1738715062,1739756401; HMACCOUNT=A534826F483F30F1; login_ucid=2000000144757586; lianjia_token=2.00155fc43e74647a8004f2ed0fa8cfa056; lianjia_token_secure=2.00155fc43e74647a8004f2ed0fa8cfa056; security_ticket=ZSXrjqCqlQw8F8QH7TmVRiwUhUlWeB0oR5mMyvBoQZD4rp/nle/nA6lkqMM60qPezMNtgDkehP6VpVB9maPlaCSK89rAoorlt2W4jK4agsGriFL1V4Wyk0Eaq/zGqbebcgy0m2KwK4TJtoCblYB3+ES0ypoFfAEtaOAoDyK4Kx0=; lianjia_ssid=3b8d46a0-403e-44b2-9407-07569c05caac; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219348819e80136e-09597493b15782-26011851-1296000-19348819e811520%22%2C%22%24device_id%22%3A%2219348819e80136e-09597493b15782-26011851-1296000-19348819e811520%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wysuzhou%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; Hm_lpvt_b160d5571570fd63c347b9d4ab5ca610=1739757717; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiYWUyYzU2OTEyZmI4MjExNzk1NmUzYTliNDRhOTk1N2I5YjRlZDI5Y2Q3Yzg3NDdlODQwMjZkMDEyMWUzMmNlOTBiYTg3YzZjNGZhNmQ5ZmNjZDQ5ODdjNDdlOGU0NWY3MjdkOWI2NWM1OTUxZTZiMDMxMWFkMDdkNzNkM2VkMWJkN2UwY2MzMzZkYzQxMmVjMDdhMmFhMzQ4ODQ5MmM1NWNiODBkNmFmNTgwNjFkMGMyYzY3MTNlYjVlNTlhZDAwZmEyOGRmZGNmYzhlMTU5MzRhZjJkZTBkYjM3ODYyNGI0MmVlNjE4ZmIxYTZkZTMxMzg2ZjhhNTRjOTcyM2Q1ZFwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCIwNjE5ZjM1N1wifSIsInIiOiJodHRwczovL3N1LmtlLmNvbS9lcnNob3VmYW5nL2MyMzk4MjE4ODc5MjMwMTUvP3N1Zz0lRTklODclOTElRTUlQkUlQTElRTUlOEQlOEUlRTUlQkElOUMiLCJvcyI6IndlYiIsInYiOiIwLjEifQ=='
}


def get_jiage(xiaoqu):
    datas = []
    if "魅力花园" in xiaoqu:
        lens = 1
        flog = "c239821887922921"
    elif "金御华府" in xiaoqu:
        lens = 1
        flog = "c239821887923015"
    else:
        return
    for u in range(0, lens):
        urls = f'https://su.ke.com/chengjiao/{flog}/'
        res = requests.get(urls, headers=headers)
        res.encoding = res.apparent_encoding
        html = etree.HTML(res.text)
        items = html.xpath('//*[@id="beike"]/div[1]/div[5]/div[1]/div[4]/ul/li')
        for i in items:
            louceng = i.xpath('./div/div[3]/div[1]/text()')[1]
            louceng2 = louceng.replace(' ', '').replace('\n', '')
            huxing = i.xpath("./div/div[1]/a/text()")[0]
            try:
                chengjiaojia = i.xpath("./div/div[2]/div[3]/span/text()")[0]
                guapai = i.xpath("./div/div[4]/span[2]/span[1]/text()")[0]
                zhouqi = i.xpath("./div/div[4]/span[2]/span[2]/text()")[0]
            except:
                guapai = i.xpath("./div/div[5]/span[2]/span[1]/text()")[0]
                zhouqi = i.xpath("./div/div[5]/span[2]/span[2]/text()")[0]
                chengjiaojia = i.xpath('./div/div[2]/div[3]/span/text()')[0]
            chengjiao_tiem = i.xpath("./div/div[2]/div[2]/text()")[0].split()[0]
            if "共18层" in louceng2:
                print(str(int(float(chengjiaojia))) + "w", "成交时间 " + chengjiao_tiem, louceng2, guapai, zhouqi, huxing)

            # jiage2 = float(jiage.replace(' ', '').replace('\n', ''))
            # url = i.xpath("./div/div[1]/a/@href")[0]
            # t = i.xpath('./div/div[2]/div[2]/text()')[1]
            # t2 = t.replace(' ', '').replace('\n', '')
            # if "魅力花园" in xiaoqu:
            #     if '共9层' in t2:
            #         datas1 = (int(jiage2), t2, url)
            #         datas.append(datas1)
            # elif "金御华府" in xiaoqu:
            datas1 = (str(int(float(chengjiaojia))) + "w", chengjiao_tiem, louceng2, guapai, zhouqi, huxing)
            datas.append(datas1)
        time.sleep(2)
    return datas


def save_data(datas, xiaoqu):
    # sorted_pairs = sorted(datas, key=lambda pair: pair[0])
    if len(datas) == 0:
        print('没有数据')
        return
    file = open('{}.csv'.format(xiaoqu), 'w', newline='', encoding='utf-8')
    for data in datas:
        writer = csv.writer(file)
        writer.writerows([data])
    print(f"{xiaoqu}CSV文件保存成功！")


if __name__ == '__main__':
    # xiaoqu = "魅力花园"
    for xiaoqu in ["金御华府"]:
        datas = get_jiage(xiaoqu)
        save_data(datas, xiaoqu + "成交")
