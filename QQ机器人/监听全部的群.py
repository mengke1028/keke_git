# -*- coding: utf-8 -*-
# Keke.Meng  2025/4/8 13:19
import websocket
import json
import time
from main import NapCatQQ


def on_message(ws, message):
    global qq_group_list
    json_data = json.loads(message)
    if '"sub_type":"connect"' in message or '"interval":30000' in message:
        pass
    else:
        json_data_list = {}
        data = ''
        data0 = ''
        if json_data['message_type'] == 'group':  # 监听qq群
            qqgroup = json_data['group_id']  # 群号
            if qqgroup not in qq_group_list:
                qq_group_list = qq.get_group_list()
            user_qq = json_data['user_id']  # 发消息的人QQ
            user_name = json_data['sender']['nickname']  # 发消息的人网名
            tims = json_data['time']  # 发消息的时间
            for datas in json_data['message']:
                if datas['type'] == 'text':
                    data0 = datas['data']['text']
                elif datas['type'] == 'face':
                    data0 = datas['data']['raw']['faceText']
                elif datas['type'] == 'image':
                    data0 = datas['data']['url']
                elif datas['type'] == 'at':
                    data0 = '@' + datas['data']['qq']
                data += data0
            json_data_list['QQ群'] = qq_group_list[qqgroup] + f"({qqgroup})"
            json_data_list['QQ号'] = user_qq
            json_data_list['昵称'] = user_name
            local_time = time.localtime(int(tims))
            # 按照指定格式将结构化时间对象转换为字符串
            formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
            json_data_list['发送时间'] = formatted_time
            json_data_list['消息内容'] = data
            print('收到群消息', json_data_list)
            # data = json_data_list
            # data['QQ群'] = '隐藏'
            # qq.send_group_msg(qqgroup='914103666', message=str(data))  # 给指定群发送群消息


        elif json_data['message_type'] == 'private':  # 监听qq私聊
            data = ''
            user_qq = json_data['user_id']  # 发消息的人QQ
            user_name = json_data['sender']['nickname']  # 发消息的人网名
            tims = json_data['time']  # 发消息的时间
            for datas in json_data['message']:
                if datas['type'] == 'text':
                    data0 = datas['data']['text']
                elif datas['type'] == 'face':
                    data0 = datas['data']['raw']['faceText']
                elif datas['type'] == 'image':
                    data0 = datas['data']['url']
                elif datas['type'] == 'at':
                    data0 = '@' + datas['data']['qq']
                elif datas['type'] == 'reply':
                    data0 = ''

                data += data0
            json_data_list['QQ号'] = user_qq
            json_data_list['昵称'] = user_name
            local_time = time.localtime(int(tims))
            # 按照指定格式将结构化时间对象转换为字符串
            formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
            json_data_list['发送时间'] = formatted_time
            json_data_list['消息内容'] = data
            print('收到私聊', json_data_list)

def on_error(ws, error):
    # print(f"发生错误: {error}")
    pass

def on_close(ws, close_status_code, close_msg):
    print("连接已关闭")


def on_open(ws):
    print("连接已建立, 开始监听QQ消息")


if __name__ == "__main__":
    qq = NapCatQQ()
    qq_group_list = qq.get_group_list()
    print(qq_group_list)
    # 定义 WebSocket 地址
    # http://192.168.188.128:6099/webui/
    ws_url = "ws://192.168.188.128:3001"
    # 创建 WebSocket 实例
    ws = websocket.WebSocketApp(ws_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    # 运行 WebSocket 客户端
    ws.run_forever()
