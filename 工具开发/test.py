import requests
headers = {
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

url = 'http://192.168.188.128:3000/get_friends_with_category'
res = requests.post(url=url,)