import random
import qqbot
import requests
print(repr(random.random()))
url = "https://ssl.ptlogin2.qq.com/ptqrlogin?u1=https%3A%2F%2Fqzs.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&ptqrtoken=1557201692&ptredirect=0&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0-1729666526.3604429&js_ver=20032614&js_type=1&login_sig=&pt_uistyle=40&aid=549000912&daid=5&"
cookies = {'qrsig': '0a9996754864afeabf9e48f3a461d2f2082cced7d4ddce10e77fc4ffdd04393d2deef41edea8d3316de47792462117617b53d1040908c90f'}
res = requests.get(url=url, cookies=cookies)
print(res)
