from selenium import webdriver
import json


def save_cookie(urls, drivers):
    drivers.get(urls)
    input("登录完成后，按回车保存cookie....")
    json_str = json.dumps(drivers.get_cookies(), ensure_ascii=False, indent=4)
    with open("cookie.json", 'w') as c:
        c.write(json_str)
    drivers.close()


def load_cookie(urls, drivers):
    drivers.get(urls)
    with open(r'cookie.json', 'r') as f:
        cookie_list = json.load(f)
        for cookie in cookie_list:
            drivers.add_cookie(cookie)
    drivers.get(urls)
    input()


if __name__ == '__main__':
    driver = webdriver.Edge()
    url = "https://su.ke.com/?utm_source=baidu&utm_medium=pinzhuan&utm_term=biaoti&utm_content=biaotimiaoshu&utm_campaign=wysuzhou"
    # save_cookie(url, driver)
    load_cookie(url, driver)
