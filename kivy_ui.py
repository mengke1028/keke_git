# -*- coding: utf-8 -*-
# Keke.Meng  2025/1/3 9:14
import kivy
import threading
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Ellipse
from kivy.properties import ListProperty
import android
kv = """
<CircleButton>:
    size_hint: None, None
    size: 200, 200
    halign: 'center'
    valign: 'center'
    text_size: self.size
"""
BUTTON_RADIUS = 100
import requests
from lxml import etree
import time

def get_dizhen():
    print('111111111111111111111111111')
    url = 'https://news.ceic.ac.cn/index.html'
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    # print(res.text)

    html = etree.HTML(res.text)
    items = html.xpath('//*[@id="news"]/table/tr')
    x = 0
    for i in items:
        if x == 0:
            x += 1
            continue

        diqu2 = i.xpath('./td[6]/a/text()')[0]
        zhenji = i.xpath('./td[1]/text()')[0]
        shijian = i.xpath('./td[2]/text()')[0]
        if '宁夏' in diqu2:
            print('地震了！！！')

            print(shijian, " " + zhenji + '级', diqu2)
            return True
        print('最新无地震')
        time.sleep(10)
        break
    return None

Flag = True
# 修改后的函数定义，添加参数以接收kivy传入的触发事件的对象
def monitoring_loop():
    global Flag
    while Flag:
        print(Flag)
        if get_dizhen():
            Flag = False
            vibrator = android.Android().vibrator()
            vibrator.vibrate(10000)  # 震动1000毫秒（1秒）

            return True

def start_monitoring(instance):
    global Flag
    Flag = True
    print("开始监测功能被调用")
    # 将开始按钮的颜色设置为绿色
    instance.background_color = [0, 1, 0, 1]
    instance.text = "Monitoring"
    thread = threading.Thread(target=monitoring_loop)
    thread.start()

def stop_monitoring(instance):
    global Flag
    print("停止监测功能被调用")
    # 将开始按钮的颜色设置为默认颜色（这里假设默认颜色为白色）
    start_button.background_color = [1, 1, 1, 1]
    start_button.text = "START "
    Flag = False

class CircleButton(Button):
    # 定义按钮的颜色属性，默认为白色
    button_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 绑定按钮大小改变事件，以便在按钮大小改变时重新绘制圆形
        self.bind(size=self.redraw_circle)

    def redraw_circle(self, instance, value):
        # 清除之前绘制的图形
        self.canvas.before.clear()
        with self.canvas.before:
            # 设置填充颜色为按钮的颜色属性
            Color(*self.button_color)
            # 绘制圆形，以按钮中心为圆心，使用固定半径100绘制
            Ellipse(pos=(self.center_x - BUTTON_RADIUS, self.center_y - BUTTON_RADIUS),
                    size=(2 * BUTTON_RADIUS, 2 * BUTTON_RADIUS))
class MyWidget(BoxLayout):
    def __init__(self):
        super().__init__()
        layout = BoxLayout(orientation='vertical')

        global start_button
        start_button = CircleButton(text="START", size_hint=(1, 0.5))
        start_button.bind(on_press=start_monitoring)
        layout.add_widget(start_button)

        stop_button = Button(text="STOP", size_hint=(1, 0.5))
        stop_button.bind(on_press=stop_monitoring)
        layout.add_widget(stop_button)

        self.add_widget(layout)


class MyApp(App):
    def build(self):
        return MyWidget()


if __name__ == '__main__':
    MyApp().run()