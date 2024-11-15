import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import os


def save_cookies(driver, path):
    with open(path, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)


def load_cookies(driver, path):
    if not os.path.exists(path):
        return False
    with open(path, 'rb') as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            # 确保只添加与当前域名匹配的 Cookie
            if 'domain' in cookie and cookie['domain'] == driver.current_url.split('//')[1].split('/')[0]:
                driver.add_cookie(cookie)
    return True


# 配置Edge选项
edge_options = EdgeOptions()
edge_options.use_chromium = True

# 创建WebDriver实例
driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=edge_options)

# 设置Cookies文件存储位置
cookies_path = "cookies.pkl"

# 尝试加载Cookies
driver.get("https://su.ke.com/?utm_source=baidu&utm_medium=pinzhuan&utm_term=biaoti&utm_content=biaotimiaoshu&utm_campaign=wysuzhou")
if not load_cookies(driver, cookies_path):
    # 如果没有找到Cookies，则手动登录并保存Cookies
    input("请完成登录操作后按回车继续...")
    save_cookies(driver, cookies_path)
else:
    # 已经有Cookies了，刷新页面以应用Cookies
    driver.get(
        "https://su.ke.com/?utm_source=baidu&utm_medium=pinzhuan&utm_term=biaoti&utm_content=biaotimiaoshu&utm_campaign=wysuzhou")

input()
# 继续你的操作...
