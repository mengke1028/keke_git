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
    "cookie": 'lianjia_uuid=e52223fe-18af-4b0f-bcc1-695078d15038; ftkrc_=d43cf478-05ba-42f8-9488-e3b40f9562f6; lfrc_=74adbdd7-55a5-408d-bf02-81b2a04a0d86; select_city=320500; Hm_lvt_b160d5571570fd63c347b9d4ab5ca610=1743384427,1745203174,1745825448; HMACCOUNT=D626EA63E6B9D7B5; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22195e9cf386ca5a-0a662cde17e5b3-26011d51-1296000-195e9cf386d2153%22%2C%22%24device_id%22%3A%22195e9cf386ca5a-0a662cde17e5b3-26011d51-1296000-195e9cf386d2153%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E4%BB%98%E8%B4%B9%E5%B9%BF%E5%91%8A%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Fother.php%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E8%B4%9D%E5%A3%B3%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wysuzhou%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; login_ucid=2000000144757586; lianjia_token=2.0014de329775e58c2905731ba618b90673; lianjia_token_secure=2.0014de329775e58c2905731ba618b90673; security_ticket=K+9rB8bk3bOjpUdl3yHUWEzK/jB+yGiXH7OhJH0HC/DBODbCD/91bB6aPLMfSwKshBWGsxfAfaz1dazHaERedWyKQom+yXTwVk5OrwiK3psnYVf/LQFRE9oUYlLd9Y2hPrj8NMJsW0BOATgbBWf5rYfx5h3AY6p4cFYJrWlgL08=; lianjia_ssid=78b79273-756c-4f9e-8a71-c4bebba72978; Hm_lpvt_b160d5571570fd63c347b9d4ab5ca610=1745825511; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiMDQ5NWI0YTZmMTdkMzkyZjVkNWQwZWVkMjY1NTQ2MGQzOTdjMzkyYWQ1NDc4NTM3NWQwNGE4OTY5NzAwMjQyMTVkZjkxZWI1MDFjN2JlYTE0ZDRkMmI2Y2NhZWFiMzRmNTNhMGRjNGE4Y2QwMGNkNjA5YzVhOTJhNjY0Y2QxMWZlYjc4NDliNjg5MjJiNjM0YjllNTU4YjFlM2FmMjA0MTg3MzYxZTY3OTZmMDQ3YWI2NzEzNzIwMGYxMDI4Mzg5OGU3ODI0ZGE3M2QyZTJkNzYyMDQwYTMwY2Y2ZmY0Y2I1NTczODg4ODQwNjVjMTNhYzE0YWU5NmYzNmNiNWIxNFwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCIxNGM0MjM2YlwifSIsInIiOiJodHRwczovL3N1LmtlLmNvbS8/dXRtX3NvdXJjZT1iYWlkdSZ1dG1fbWVkaXVtPXBpbnpodWFuJnV0bV90ZXJtPWJpYW90aSZ1dG1fY29udGVudD1iaWFvdGltaWFvc2h1JnV0bV9jYW1wYWlnbj13eXN1emhvdSIsIm9zIjoid2ViIiwidiI6IjAuMSJ9'
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
