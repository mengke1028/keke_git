from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import threading
from selenium.webdriver.edge.options import Options


def login(use, pwd):
    # 自动下载并安装 Edge 驱动程序
    # edge_options = Options()
    # edge_options.add_argument('--headless')
    # edge_options.add_argument('--disable-gpu')  # 禁用 GPU 加速，某些情况下可能需要
    # edge_options.add_argument('--no-sandbox')  # 禁用沙箱模式，某些情况下可能需要
    # edge_options.add_argument('--disable-dev-shm-usage')  # 禁用 /dev/shm 使用，某些情况下可能需要
    #
    # # 初始化 WebDriver（以 Edge 为例）
    # driver = webdriver.Edge(options=edge_options)
    edge_options = Options()
    user_data_dir = r"C:\Users\Keke.Meng\AppData\Local\Microsoft\Edge\UserData"  # 替换为你的用户数据目录路径
    edge_options.add_argument(f'--user-data-dir={user_data_dir}')

    driver = webdriver.Edge(options=edge_options)
    # 尝试加载Cookies
    driver.get("http://sclpa.mtnet.com.cn/login")
    wait = WebDriverWait(driver, 10)  # 最多等待 10 秒
    username_input = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="loginPc"]/div/div/div[2]/div[1]/input')))

    # 输入账号
    username_input.send_keys(use)  # 请替换为实际的用户名
    import time
    time.sleep(1)
    pwd_input = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="loginPc"]/div/div/div[2]/div[2]/input')))
    pwd_input.send_keys(pwd)  # 请替换为实际的用户名

    time.sleep(1)
    login = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="loginPc"]/div/div/div[2]/button')))
    login.click()
    time.sleep(1)

    driver.get('http://sclpa.mtnet.com.cn/user/study')
    wait = WebDriverWait(driver, 10)  # 最多等待 10 秒

    click_2024 = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="indexPage"]/div/div/div[2]/div/div[2]/div/div/div[2]/ul/li[1]')))
    click_2024.click()

    try:
        name = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div/div[1]/div[1]/div/div[2]')))
        print(name.text)
    except:
        pass

    input()
    time.sleep(10000)
    # 继续你的操作...


# 账号和密码列表
accounts = [
    # ('513124197202076160', '12345'),
    ('510122197108187512', '12345'),
    # ("510125198011070063", 'denglan978846'),
    # ("511321198410113733", '12345')
]

# 创建并启动线程
threads = []
for account, password in accounts:
    thread = threading.Thread(target=login, args=(account, password))
    threads.append(thread)
    thread.start()

# 等待所有线程完成
for thread in threads:
    thread.join()

print("All browsers have completed their tasks.")
