import requests
from urllib import parse

# data='{"req":{"module":"CDN.SrfCdnDispatchServer",\
# "method":"GetCdnDispatch","param":{"guid":"6522780672","calltype":0,"userip":""}},\
# "req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"6522780672",\
# "songmid":["%s"],"songtype":[0],"uin":"0","loginflag":1,\
# "platform":"20"}},"comm":{"uin":0,"format":"json","ct":24,"cv":0}}' %'000gnHiB3wKUKz'


data = {"comm": {"cv": 4747474, "ct": 24, "format": "json", "inCharset": "utf-8", "outCharset": "utf-8", "notice": 0,
                 "platform": "yqq.json", "needNewCode": 1, "uin": "1152921504796895114",
                 "g_tk_new_20200303": 1837467563, "g_tk": 1837467563},
        "req_1": {"module": "music.trackInfo.UniformRuleCtrl", "method": "CgiGetTrackInfo",
                  "param": {"types": [0, 0, 0], "ids": [106359731, 215540451, 299483580]}},
        "req_2": {"module": "music.musicasset.SongFavRead", "method": "IsSongFanByMid",
                  "param": {"v_songMid": ["000P8peU0HhORi", "003jjoM94WLiTf", "004d8TPg3Sn98k"]}},
        "req_3": {"module": "music.musichallSong.PlayLyricInfo", "method": "GetPlayLyricInfo",
                  "param": {"songMID": "000P8peU0HhORi", "songID": 106359731}},
        "req_4": {"method": "GetCommentCount", "module": "music.globalComment.GlobalCommentRead",
                  "param": {"request_list": [{"biz_type": 1, "biz_id": "106359731", "biz_sub_type": 0}]}},
        "req_5": {"module": "music.musichallAlbum.AlbumInfoServer", "method": "GetAlbumDetail",
                  "param": {"albumMid": "002obDH53uiSTk"}},
        "req_6": {"module": "music.vkey.GetVkey", "method": "GetUrl",
                  "param": {"guid": "8935571292", "songmid": ["000P8peU0HhORi"], "songtype": [0],
                            "uin": "1152921504796895114", "loginflag": 1, "platform": "20"}}}

url = "https://u.y.qq.com/cgi-bin/musicu.fcg?-=getplaysongvkey2091814222203221&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data=%7B%22req%22%3A%7B%22module%22%3A%22CDN.SrfCdnDispatchServer%22%2C%22method%22%3A%22GetCdnDispatch%22%2C%22param%22%3A%7B%22guid%22%3A%226522780672%22%2C%22calltype%22%3A0%2C%22userip%22%3A%22%22%7D%7D%2C%22req_0%22%3A%7B%22module%22%3A%22vkey.GetVkeyServer%22%2C%22method%22%3A%22CgiGetVkey%22%2C%22param%22%3A%7B%22guid%22%3A%226522780672%22%2C%22songmid%22%3A%5B%22000gnHiB3wKUKz%22%5D%2C%22songtype%22%3A%5B0%5D%2C%22uin%22%3A%220%22%2C%22loginflag%22%3A1%2C%22platform%22%3A%2220%22%7D%7D%2C%22comm%22%3A%7B%22uin%22%3A0%2C%22format%22%3A%22json%22%2C%22ct%22%3A24%2C%22cv%22%3A0%7D%7D"
respose = requests.get(url).json()
print(respose)
vkey = (respose['req']['data']['vkey'])
# vkey = ''
headers = {
    "accept": "*/*",
    "accept-encoding": "identity",
    "accept-language": "zh-CN,zh;q=0.9",
    "if-range": "'a59c7d479525f2d4ac467140c2f571175464b34d'",
    "origin": "https://y.qq.com",
    "priority": "u=1, i",
    "range": "bytes=368640-737279",
    "referer": "https://y.qq.com/",
    "sec-ch-ua": "'Google Chrome';v='131', 'Chromium';v='131', 'Not_A Brand';v='24'",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "'Windows'",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}

url_2 = 'https://ws6.stream.qqmusic.qq.com/C400001L1mv24ORYiL.m4a?guid=8315465960&vkey={}&uin=1152921504796895114&fromtag=120032'.format(
    vkey)
print(url_2)
reps = requests.get(url=url_2, headers=headers)
print(reps)
