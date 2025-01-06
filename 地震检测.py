# -*- coding: utf-8 -*-
# Keke.Meng  2025/1/3 8:30
import requests
from lxml import etree
import re


def get_dizhen():
    url = 'https://news.ceic.ac.cn/index.html'
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    # print(res.text)

    html = etree.HTML(res.text)
    items = html.xpath('//*[@id="news"]/table/tr')
    x = 0
    for i in items:
        if x == 0:
            x += 1
            continue

        diqu2 = i.xpath('./td[6]/a/text()')[0]
        zhenji = i.xpath('./td[1]/text()')[0]
        shijian = i.xpath('./td[2]/text()')[0]
        if '宁夏' in diqu2:
            print('地震了！！！')
            print(shijian, " " + zhenji + '级', diqu2)
            return True
        else:
            print('最新无地震')
        break
    return None


def dizhenlishi():
    url = 'https://news.ceic.ac.cn/speedsearch.html'
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    # print((res.text).encode('utf-8').decode('unicode_escape'))
    html = etree.HTML((res.text).encode('utf-8').decode('unicode_escape'))
    script_elements = html.xpath('//script')
    for script in script_elements:
        script_text = script.text
        if script_text and "const newdata =" in script_text:
            # 这里可以进一步提取newdata具体的值，比如如果newdata后面跟着具体的值，假设是用引号包裹的字符串
            start_index = script_text.find("const newdata =") + len("const newdata =")
            value = script_text[start_index:].strip().strip(';').strip("'").strip('"')
            value = value[2:-25]
            d = value.split('},{')
            for x in d:
                dengji = x[5:8]
                shijian = x[20:39]
                pattern = r'LOCATION_C":"(.*?)"'
                matches = re.findall(pattern, x)
                if matches:
                    if '宁夏' in matches[0]:
                        print(shijian, dengji + "级", matches[0])

    # for i in value:
    #     print(i)
    #     break


if __name__ == '__main__':
    print('宁夏最近一年的地震活动 2025.1.3')
    dizhenlishi()
