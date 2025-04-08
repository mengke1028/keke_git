# -*- coding: utf-8 -*-
# Keke.Meng  2025/4/8 9:47
import requests
import json
import time


class NapCatQQ:
    def __init__(self):
        self.url = 'http://192.168.188.128:3000/'
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "authorization": "Bearer 111111",
            "connection": "keep-alive",
            "content-length": "2",
            "content-type": "application/json",
            "host": "127.0.0.1:3000",
            "origin": "http://127.0.0.1:6099",
            "referer": "http://127.0.0.1:6099/",
            "sec-ch-ua": "'Microsoft Edge';v='135', 'Not-A.Brand';v='8', 'Chromium';v='135'",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "'Windows'",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
        }

    def get_friend_list(self):
        """获取好友列表 QQ和昵称"""
        data_list = {}
        url = self.url + '/get_friend_list'
        data = {
            "no_cache": 'false'
        }
        res = requests.post(url, headers=self.headers, json=data)
        all_data = res.json()
        if all_data['status'] == 'ok':
            for i in all_data['data']:
                print(f"{i['user_id']:10}", f"{i['nickname']:15}")
                data_list[i['user_id']] = i['nickname']
        return data_list

    def send_private_msg(self, qq, message=''):
        """给指定qq号发送私聊消息"""
        url = self.url + '/send_private_msg'

        data = {
            "user_id": qq,
            "message": [
                {
                    "type": "text",
                    "data": {
                        "text": f"{message}\n"
                    }
                }
            ]
        }
        res = requests.post(url, headers=self.headers, json=data)
        print(res.text)

    def send_group_msg(self, qqgroup, message=''):
        """给指定qq群号发送私聊消息"""
        url = self.url + '/send_group_msg'

        data = {
            "group_id": qqgroup,
            "message": [
                {
                    "type": "text",
                    "data": {
                        "text": f"{message}\n"
                    }
                }
            ]
        }
        res = requests.post(url, headers=self.headers, json=data)
        print(res.text)

    def get_group_list(self, next_token='2'):
        """获取群列表"""
        data_list = {}
        url = self.url + '/get_group_list'
        data = {
            "next_token": next_token
        }
        res = requests.post(url, headers=self.headers, json=data)
        all_data = res.json()
        if all_data['status'] == 'ok':
            for i in all_data['data']:
                # print(f"{i['group_id']:10}", f"{i['group_name']:15}")
                data_list[i['group_id']] = i['group_name']
        return data_list

    def get_group_msg_history(self, qqgroup):
        """读取群最新消息"""
        data_list = {}
        url = self.url + '/get_group_msg_history'
        data = {
            "group_id": qqgroup,
            "message_seq": '',
            "count": 10,
            "reverseOrder": 'true'
        }

        res = requests.post(url, headers=self.headers, json=data)
        all_data = res.json()
        # 使用 json.dumps() 格式化输出
        formatted_data = json.dumps(all_data, indent=4, ensure_ascii=False)
        if all_data['status'] == 'ok':
            for i in all_data['data']['messages']:
                # print(f"{i['group_id']:10}", f"{i['group_name']:15}")
                if i['sender']['card'] == '':  # 群昵称位空
                    data_list['网名'] = i['sender']['nickname']
                else:
                    data_list['网名'] = i['sender']['card']

                data_list['QQ号'] = i['user_id']
                local_time = time.localtime(int(i['time']))
                # 按照指定格式将结构化时间对象转换为字符串
                formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
                data_list['发送时间'] = formatted_time
                if not i['message']:
                    data_list['发送的消息'] = '消息可能被撤回'
                else:
                    if i['message'][0]['type'] == 'text':
                        data_list['发送的消息'] = i['message'][0]['data']['text']
                    elif i['message'][0]['type'] == 'face':
                        data_list['发送的消息'] = i['message'][0]['data']['raw']['faceText']
                    elif i['message'][0]['type'] == 'image':
                        data_list['发送的消息'] = i['message'][0]['data']['url']

                print(data_list)
        return data_list


if __name__ == '__main__':
    napcatqq = NapCatQQ()
    # all_qq = napcatqq.get_friend_list()  # 查看全部qq好友
    # print(all_qq)
    # napcatqq.send_private_msg(qq='1419401541',message='qq机器人测试1')  # 给指定qq发送消息
    #
    # napcatqq.send_group_msg(qqgroup='778631068', message='qq机器人测试1')  # 给指定群发送群消息

    group_list = napcatqq.get_group_list()  # 获取所有群列表
    print(group_list)
    data_list = napcatqq.get_group_msg_history(qqgroup='778631068')  # 获取指定群消息群消息
    print(data_list)
