import requests
import base64

headers = {
 'Connection':'keep-alive',
 'Content-Length':'348',
 'Cache-Control':'max-age=0',
 'Upgrade-Insecure-Requests':'1',
 'Origin':'http://wx.jssz12320.cn',
 'Content-Type':'application/x-www-form-urlencoded',
 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090c37) XWEB/14185 Flue',
 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/wxpic,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
 'Referer':'http://wx.jssz12320.cn/gh/register/normalPool.ha?hospName=%E8%8B%8F%E5%B7%9E%E5%B8%82%E5%A6%87%E5%B9%BC%E4%BF%9D%E5%81%A5%E9%99%A2&departName=%E5%A6%87%E7%A7%91%EF%BC%88%E6%97%A9%E5%AD%95%E5%85%B3%E7%88%B1%EF%BC%89%E6%99%AE%E9%80%9A%E9%97%A8%E8%AF%8A&workDate=2026-01-17&workType=%E4%B8%8A%E5%8D%88',
 'Accept-Encoding':'gzip, deflate',
 'Accept-Language':'zh-CN,zh;q=0.9',
 'Cookie':'userId=o6FXZjuLg1FbSrJVM0lRUrDUeIjU; userStr=R9nnF4vuP6LBJX9t6j39ddSMBBB3X6rFXx1lHLE4OHhFlx1tPEbTYsnQBDut%2BFNva8wQvFt%2BmqzB%0D%0AXyF5AJYX%2BLpsko94iBY1YUtKg%2BZwvjaYjxoQXZMF3d%2FrdTkl3%2FR91vwkLEkQgo9FGWt7NyI3eqzf%0D%0A8lBC8XvBBLOHMmyGWo042SrNqS8knlIWDLUKQUoJYndrcvHgP%2Bu91Kxb%2FjqjeRpr%2BaedtTjYQUFb%0D%0AHfizBxnhHx3BUwsj0kLwagfHew6nvce7%2FNVw%2F4ithFwBWGcOtZKuwvsa18VW3%2Ftn5rn1r3P5DIyZ%0D%0ApCzLl2%2FaUb%2BRpiql6hkYQ0rqrJP4f2I06sSC5cewl5Q473qJqid1AxgbCvobLs4V%2BQoQPJl7LRGA%0D%0AIxLkAFSGbHK8Zur94J7tqnJ2dew5%2BSTotV4Gs2bjvbcNCEH0vAU92DRjZTqesxiuwJrzzqq8QSbK%0D%0AeDP8hHUpvvjxvg%3D%3D; needAlert=1; SESSION=69d3043f-60bd-4170-a672-3426e49e15fd'}
payload=base64.b64decode("aG9zcE5hbWU9JUU4JThCJThGJUU1JUI3JTlFJUU1JUI4JTgyJUU1JUE2JTg3JUU1JUI5JUJDJUU0JUJGJTlEJUU1JTgxJUE1JUU5JTk5JUEyJmRlcGFydE5hbWU9JUU1JUE2JTg3JUU3JUE3JTkxJUVGJUJDJTg4JUU2JTk3JUE5JUU1JUFEJTk1JUU1JTg1JUIzJUU3JTg4JUIxJUVGJUJDJTg5JUU2JTk5JUFFJUU5JTgwJTlBJUU5JTk3JUE4JUU4JUFGJThBJndvcmtEYXRlPTIwMjYtMDEtMTcmd29ya1R5cGU9JUU0JUI4JThBJUU1JThEJTg4JmJlZ2luVGltZT0xMCUzQTMwJmVuZFRpbWU9MTElM0EwMCZhZHZpY2VTdGFydEZldGNoVGltZT0xMCUzQTAwJmFkdmljZUVuZEZldGNoVGltZT0xMCUzQTMwJnJlZ1R5cGU9")

response0 = requests.request("POST", "http://wx.jssz12320.cn/gh/register/register.ha", headers=headers, data=payload)
print(response0.text)


