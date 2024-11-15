from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

# 设置 Desired Capabilities
desired_caps = {
    'platformName': 'Android',
    'deviceName': 'emulator-5554',
    # 'appPackage': 'com.tencent.qqmusic',
    # 'appActivity': '.activity.AppStarterActivity',
    # 'noSign': False
}

# 启动 Appium 会话
try:
    options = UiAutomator2Options().load_capabilities(desired_caps)
    driver = webdriver.Remote('http://localhost:4723/wd/hub', options=options)
    print("Driver initialized successfully.")
except Exception as e:
    print(f"Error initializing driver: {e}")
    raise
print("初始化成功")
element = driver.find_element(AppiumBy.XPATH, '//*[contains(@text,"要闻")]')
print(element.text)

# try:
#     element = driver.find_element(AppiumBy.XPATH, '//*[contains(@text, "QQ音乐")]')
#     element.click()
#     print("Element with text 'QQ音乐' found and clicked.")
# except:
#     print('<<QQ音乐>> 没找到')
# try:
#     wode = driver.find_element(AppiumBy.XPATH, '//*[contains(@text, "我的")]')
#     wode.click()
#     print("点击 <<我的>>")
# except:
#     print('<<我的>> 没找到')
#：
# try:
#     wode = driver.find_element(AppiumBy.XPATH, '//*[contains(@text, "提现")]')
#     wode.click()
#     print("点击 <<提现>>")
# except:
#     print('<<提现>> 没找到')

