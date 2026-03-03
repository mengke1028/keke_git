
# -*- coding: utf-8 -*-
# TCN01475  2026/3/3 8:32
import requests
import csv
import time

def new_url(id, xsec_token):
    return f'https://www.xiaohongshu.com/explore/{id}?xsec_token={xsec_token}&xsec_source=pc_search'


urls = 'https://edith.xiaohongshu.com/api/sns/web/v1/search/notes'

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-length": "191",
    "content-type": "application/json;charset=UTF-8",
    "cookie": "a1=19a9aefcca7m15zwdi3j1bs5rwb0q1l9ya6vvzu6i50000337472; webId=768afeffdf8baa2e0240f1d20abcf42e; abRequestId=768afeffdf8baa2e0240f1d20abcf42e; gid=yj0j0iyfDjvjyj0j0diSS0u70W6y2uEf3qVyKK3DM2FEDh288Ay1jh888qqW4WJ8iy2S8JSq; web_session=0400698d6cf3434616192caf5c3b4b71cefa56; id_token=VjEAAJalQzzPMIDoXbetuN5STjmZ0zdoe+dkOdTxrGldt3603hfHFi7Dke+xP1kS9ZVctHvnTEuOcAfZhuW3EeFnMHxwu0c8PS0zCuZvIzIGzy4wEddbl3z3r6DnKiEG0upq+jZq; xsecappid=xhs-pc-web; webBuild=5.13.0; acw_tc=0a4a119f17724315704557438e14a9416a02aed5168117f80853121792b09d; unread={%22ub%22:%2269a00294000000002203332e%22%2C%22ue%22:%226995bd3d000000000a02d780%22%2C%22uc%22:25}; websectiga=984412fef754c018e472127b8effd174be8a5d51061c991aadd200c69a2801d6; sec_poison_id=01aa1550-b344-4da6-87d6-25ee41553cad; loadts=1772431966730",
    "origin": "https://www.xiaohongshu.com",
    "priority": "u=1, i",
    "referer": "https://www.xiaohongshu.com/",
    "sec-ch-ua": "\"Not:A-Brand\";v=\"99\", \"Google Chrome\";v=\"145\", \"Chromium\";v=\"145\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    "x-b3-traceid": "85c1de0083cd894b",
    "x-s": "XYS_2UQhPsHCH0c1PUhlHjIj2erjwjQhyoPTqBPT49pjHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQTJdPIPAZlg94aGLTl4nkpcfHItM4fanzbPAmk8rSby9QUt9Qawepn+n4x2bSkzLDUy0bf+FDF8rpxprFUynQ3qLu6LgSI+bp/4pQyGfMyLgrI/nzHcdYV/0YULeQk/FGIJsTx/eLl8Dlh/L+nySkLP0mpagq7wrRB89kmPrkHaMY/+7YnwBSTPn8+c9EIqMQCLDkcpnbLP9I74DT/Jfznnfl0yFLIaSQQyAmOarEaLSz+qFhEGfbFyfEyJ0878BV32gYxq7ptJaHVHdWFH0ijJ9Qx8n+FHdF=",
    "x-s-common": "2UQAPsHC+aIjqArjwjHjNsQhPsHCH0rjNsQhPaHCH0c1PUhlHjIj2eHjwjQgynEDJ74AHjIj2ePjwjQhyoPTqBPT49pjHjIj2ecjwjHMN0rAN0ZjNsQh+aHCH0rEG/SY8n80G9r7J/rM2d4Dy/+xPnQA+gQ7G0mlPnIE2nr94d8C4/8k+/ZIPeZAPAqF+AHjNsQh+jHCHjHVHdW7H0ijHjIj2eWjwjQQPAYUaBzdq9k6qB4Q4fpA8b878FSet9RQzLlTcSiM8/+n4MYP8F8LagY/P9Ql4FpUzfpS2BcI8nT1GFbC/L88JdbFyrSiafpr8DMra7pFLDDAa7+8J7QgabmFz7Qjp0mcwp4fanD68p40+fp8qgzELLbILrDA+9p3JpH9LLI3+LSk+d+DJfpSL98lnLYl49IUqgcMc0mrcDShtUTozBD6qM8FyFSh8o+h4g4U+obFyLSi4nbQz/+SPFlnPrDApSzQcA4SPopFJeQmzBMA/o8Szb+NqM+c4ApQzg8Ayp8FaDRl4AYs4g4fLomD8pzBpFRQ2ezLanSM+Skc47Qc4gcMag8VGLlj87PAqgzhagYSqAbn4FYQy7pTanTQ2npx87+8NM4L89L78p+l4BL6ze4AzB+IygmS8Bp8qDzFaLP98Lzn4AQQzLEAL7bFJBEVL7pwyS8Fag868nTl4e+0n04ApfuF8FSbL7SQyrLUaBRypLShJpmO2fM6anS0nBpc4F8Q4fSePDH7qFzC+7+hpdzDagG98nc7+9p8ydL3anDM8/8gGDzwqg4xanYtqA+68gP9zo8SpbmF/f+p+fpr4gqMag8889P6+9pDLo4e898OqM+c4MkQPM+YagYTJo+l4o+YLo4Eq7+HGSkm4fLAqsRSzbm72rSe8g+3zemSL9pHyLSk+7+xGfRAP94UzDSk8BL94gqAanSUy7zM4BMF4gzBagYS8pzc4r8QyrkSyp8FJrS389LILoz/t7b7Lokc4MpQ4fY3agY0q0zdarr3aLESypmFyDSiqdzQyBRAydbFLrlILnb7qDTA8B808rSi2juU4g4yqdp7LFSe8o+3Loz/tFMN8/b0cg+k/nMPanSmq7W78g+L4gzEGMm7qLSePBpfpdzpanSw8pzA4pmQcFTSnnuA8p4n4ApQ2rTAPgp74LkspMzQypS7a/+d8/+T+7+8yd8APBFI8nzM49lQznThaL+iyn+n4AYQyLzNa/P68/ZI+BECc0+S8bm7qrS3Lr4CpdqML/DMqM+V89p8pd4S8gpFnDShyeYQy/Yy/op7aAYc4eQQ2BRApfHA8gYn4eQypd4danSH47Qc4e8Qyp8D/0mPcLSkJ7+x/e+ApdZ68pzn4URwpdzVanTU2rShP7+hqgzkanY98nTI/LSQ4jTwabkbarS9wB4QyrkSLM87PfEl4Bzz4gzSanVFprS38o+gcLbAyM878sRILb4QcFDF2dpFPfMc4sTQ2orMagYzcDSknLpQc78SPFz9qM8IGDMOpd4AaL+Bp7kc47kjpd4ganYD8pSfnSSQygbGqBc98nkM4r+S4gzn/fpP8DY/p9+Q2BHhwb87pDSh8o+xPbShanYacjHVHdWEH0ilPADMPeD7+ec9NsQhP/Zjw0ZVHdWlPaHCHfE6qfMYJsHVHdWlPjHCH0r7+AHFPArE+0GhP0DvP/q7P0rhP/G9PeDhPUQR",
    "x-t": "1772431967088",
    "x-xray-traceid": "ce5696c198be4c7da466b9707c4c0de3"
}
data = {"keyword": "相城魅力花园租房", "page": 1, "page_size": 20, "search_id": "2g1w2av7k1yie3b1lgrjm", "sort": "general",
        "note_type": 0, "ext_flags": [], "geo": "", "image_formats": ["jpg", "webp", "avif"]}

with open('租房信息.csv', 'w', newline="", encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["title", "date", "url"])
    for i in range(2, 5):
        data['page'] = i
        print(data)
        res = requests.post(url=urls, headers=headers, json=data)

        datas = res.json()
        data_list = datas['data']['items']
        for i in data_list:
            try:
                xsec_token = i['xsec_token']
                title = i['note_card']['display_title']  # 帖子标题
                url = new_url(i['id'], xsec_token)  # 组合详情地址
                date = i['note_card']['corner_tag_info'][0]['text']  # 帖子日期
                data_list = [title, date, url]
                writer.writerow(data_list)  # 写入csv
            except:
                # 对于没有标题的帖子跳过
                pass

        time.sleep(1)




