# -*- coding: utf-8 -*-
# Keke.Meng  2025/10/24 11:55
import requests
from datetime import datetime, timedelta
import time

headers = {
    'Authorization': 'HnzjdNsseUWkdeKqkaQCAFkXePnVEjBG'
}


def get_http_server_time(url='https://www.baidu.com'):
    """从 HTTP 响应头获取服务器时间，转换为北京时间"""
    try:
        # 发送 HEAD 请求（仅获取响应头，不下载内容）
        response = requests.head(url, timeout=5)
        # 提取响应头中的 Date 字段（UTC 时间）
        date_str = response.headers.get('Date')
        if not date_str:
            return None
        # 解析为 UTC 时间（格式示例："Fri, 24 Oct 2025 08:00:00 GMT"）
        utc_time = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S GMT")
        # 转换为北京时间（UTC+8）
        beijing_time = utc_time + timedelta(hours=8)
        server_time = str(beijing_time)
        server_time2 = server_time[-2:]
        return server_time2
    except Exception as e:
        print(f"获取 HTTP 时间失败：{e}")
        return None


def get_data():
    url = 'https://api.lzd668.com/api/game/home/3'
    res = requests.get(url, headers=headers)
    data = res.json()
    all_list = data['list']
    draw_time = get_http_server_time()

    periodId = all_list[3]["id"]

    draw_no_arr1 = all_list[4]["draw_no_arr"][0]
    draw_no_arr2 = all_list[5]["draw_no_arr"][0]
    numb = (str(draw_no_arr1 + draw_no_arr2))[-1]

    draw_money = all_list[4]['draw_money']
    win_money = all_list[4]['win_money']
    if draw_money != '0' and win_money == '0':
        yingli = False
        print('盈利失败')
    else:
        yingli = True
        print('盈利成功')
    datas = {
        'draw_time': draw_time,  # 结束时间
        'periodId': periodId,  # 下注ID
        'numb': numb,  # 避免下注的号码
        'yingli': yingli  # 是否盈利成功
    }
    return datas


def get_periodId():
    url = 'https://api.lzd668.com/api/game/home/3'
    headers = {
        'Authorization': 'HnzjdNsseUWkdeKqkaQCAFkXePnVEjBG'
    }
    res = requests.get(url, headers=headers)
    data = res.json()
    all_list = data['list']
    draw_no_arr1 = all_list[3]["id"]
    return draw_no_arr1


def xiazhu(numb, periodId, xiazhuer=5193):
    url = 'https://api.lzd668.com/api/game/gameJoin/3'

    dange_xiahuer = str(int(xiazhuer / 9))

    bet_num = [dange_xiahuer, dange_xiahuer, dange_xiahuer, dange_xiahuer, dange_xiahuer, dange_xiahuer, dange_xiahuer,
               dange_xiahuer, dange_xiahuer, dange_xiahuer]
    if numb != '0':
        bet_num[int(numb) - 1] = '0'
    else:
        bet_num[9] = '0'

    json = {"bet_num": bet_num, "total": xiazhuer,
            "periodId": periodId}
    requests.post(url, headers=headers, json=json)


def RUN():
    xiazhuer = int(input("请输入投注数："))
    fanbeicishu = int(input("请输入最大翻倍次数："))
    shibaicushu = 0
    while True:
        datas = get_data()
        stop_time_numb = int(datas['draw_time'])
        if 50 > stop_time_numb > 20:
            print('可以下注')
            if datas['yingli']:
                shibaicushu = 0
            else:
                shibaicushu += 1
                if shibaicushu < fanbeicishu:
                    xiazhuer = 12 * xiazhuer
            periodId = datas['periodId']  # 下注ID
            numb = datas['numb']  # 避免下注的号码
            xiazhu(numb, periodId, xiazhuer)
            time.sleep(40)
        else:
            print(stop_time_numb, '等待5秒再判断是否下注')
            time.sleep(5)  # 等待60秒
            continue


if __name__ == '__main__':
    RUN()
