# -*- coding: utf-8 -*-
# Keke.Meng  2025/6/4 13:57
import requests
import json


def get_bilibili_video_info(bvid):
    """获取B站视频信息"""
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://www.bilibili.com/",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()

        if data["code"] == 0:
            video_info = data["data"]
            print(f"视频标题: {video_info['title']}")
            print(f"UP主: {video_info['owner']['name']}")
            print(f"播放量: {video_info['stat']['view']}")
            print(f"弹幕数: {video_info['stat']['danmaku']}")
            return video_info
        else:
            print(f"请求失败，错误码: {data['code']}，错误信息: {data['message']}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"网络请求异常: {e}")
        return None
    except json.JSONDecodeError:
        print("解析JSON响应失败")
        return None


# 使用示例
if __name__ == "__main__":
    bvid = "BV1UB7ezKEce"  # 指定要查询的视频BVID
    get_bilibili_video_info(bvid)