# -*- coding: utf-8 -*-
# Keke.Meng  2025/4/9 11:45
import os

from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from 小鱼干综合工具 import MultiPageWindow
from pynput import keyboard
from threading import Thread
import json


class MW(MultiPageWindow):
    def __init__(self):
        super().__init__()
        self.config_data = {}
        # 自动上号
        self.shanghao.clicked.connect(self.wegam_loging)  # 开始上号
        self.mimaben_path = None
        self.huoyan = None
        self.qq = None
        self.pwd = None
        self.zhixingbanzhuan = None

        # 扫拍
        self.start.clicked.connect(self.get_saopai)  # 扫拍
        self.wupin_name = None  # 扫拍物品名
        self.mubiaojiage = None  # 扫拍目标价格
        self.suijianqujian = None  # 随机时间
        self.suijianqujian2 = None  # 随机时间
        self.youdanjia = None  # 是否有单价
        self.chushihua = None  # 是否需要初始化

        # 其他
        self.gonghuika.clicked.connect(self.gonghui_fenka)  # 兑换工会粉卡
        self.duihuanbaiyu.clicked.connect(self.duihuanbaozhu)  # 兑换黄龙之白玉宝珠
        self.jilushangpin.clicked.connect(self.jilushangpinjiage)  # 记录商品价格
        self.wupinjiage_path = None
        self.lianjin_start.clicked.connect(self.lianjinshujiage)  # 记录炼金术材料价格
        self.lianjinshu_path = None

        # 搬砖
        self.banzhuan_start.clicked.connect(self.kaishibanzhuan)
        self.banzhuan_stop.clicked.connect(self.stop_all)
        self.tu = None
        self.dengji = None
        self.load_config()  # 读取配置

    def wegam_loging(self):
        """"wegame登录"""
        self.huoyan = self.huoyankami.text()  # 获取火眼的卡密
        self.qq = self.qqnumb.currentText()  # 读取选中的qq号
        self.pwd = self.qq_json[self.qq]  # 根据qq  获取密码
        self.zhixingbanzhuan = self.zhijbanzhuan.isChecked()  # 登录后直接搬砖
        self.mimaben_path = self.mima_file_path_input.text()  # 密码本路径
        self.save_config()

    def kaishibanzhuan(self):
        """开始搬砖"""
        self.banzhuan_start.setStyleSheet("""
                        QPushButton {
                            background-color: rgb(60, 70, 80); /* 颜色变浅 */
                            border: 2px solid rgb(50, 200, 210); /* 颜色变浅 */
                            height: 44px;
                            width: 180px;
                            border-radius: 30px;
                            color: rgb(50, 200, 210); /* 颜色变浅 */
                            font-size: 30px; /* 字体大两号 */
                            font-weight: bold;
                            /* 使按钮支持 checked 状态 */
                            checkable: true; 
                        }
                    """)
        self.banzhuan_start.setText('搬砖中...')
        # 设置按钮为不可用状态，防止重复点击
        self.banzhuan_start.setEnabled(False)
        self.tu = self.ditu.currentText()
        self.dengji = self.nandu.currentText()
        for i in range(30):
            self.set_banzhuan_log(self.tu, self.dengji, 123)  # 写入log
        # print(self.tu, self.dengji)
        self.save_config()

    def get_saopai(self):
        self.wupin_name = self.name.text()  # 扫拍物品名
        self.set_banzhuan_log(self.wupin_name)
        self.mubiaojiage = self.jiage.text()  # 扫拍目标价格
        self.set_banzhuan_log(self.mubiaojiage)
        self.suijianqujian = self.start_time.text()  # 随机时间
        self.set_banzhuan_log(self.suijianqujian)
        self.suijianqujian2 = self.end_time.text()  # 随机时间
        self.set_banzhuan_log(self.suijianqujian2)
        self.youdanjia = self.checkbox1.isChecked()  # 是否有单价
        self.set_banzhuan_log(self.youdanjia)
        self.chushihua = self.checkbox2.isChecked()  # 是否需要初始化
        self.set_banzhuan_log(self.chushihua)
        self.save_config()

    def gonghui_fenka(self):
        """开始兑换工会粉卡"""

    def duihuanbaozhu(self):
        """"兑换黄龙宝珠"""

    def jilushangpinjiage(self):
        """记录商品价格"""
        self.wupinjiage_path = self.file_path_input.text()  # 获取文本框内容
        self.save_config()

    def lianjinshujiage(self):
        """记录炼金术价格"""
        self.lianjinshu_path = self.lianjin_file_path_input.text()  # 获取文本框内容
        self.save_config()

    def stop_all(self):
        """停止一切进程"""
        self.banzhuan_start.setStyleSheet(self.button_style)
        self.banzhuan_start.setEnabled(True)
        self.banzhuan_start.setText('开始')
        self.set_banzhuan_log('停止搬砖')  # 写入log

    def on_press(self, key):
        try:
            if key == keyboard.Key.home:
                print('home')
                self.stop_all()
                # 你可以在这里添加其他操作

        except AttributeError:
            pass

    def start_global_key_listener(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

    def save_config(self):
        """保存全部配置"""
        self.config_data = {'huoyan': self.huoyankami.text(),  # 火眼卡密
                            'qq': self.qqnumb.currentText(),  # QQ号
                            'zhixingbanzhuan': self.zhijbanzhuan.isChecked(),  # 登录后直接搬砖
                            'mimaben_path': self.mima_file_path_input.text(),  # 密码路径
                            'wupin_name': self.name.text(),  # 扫拍物品名
                            'mubiaojiage': self.jiage.text(),  # 扫拍目标价格
                            'suijianqujian': self.start_time.text(),  # 随机时间
                            'suijianqujian2': self.end_time.text(),  # 随机时间
                            'youdanjia': self.checkbox1.isChecked(),  # 是否有单价
                            'chushihua': self.checkbox2.isChecked(),  # 是否需要初始化
                            'wupinjiage_path': self.file_path_input.text(),  # 商品价格路径
                            'lianjinshu_path': self.lianjin_file_path_input.text(),  # 炼金术价格路径
                            'tu': self.ditu.currentText(),  # 搬砖地图
                            'dengji': self.nandu.currentText()  # 难度等级
                            }

        try:
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=4)
        except Exception as e:
            print(f"保存配置文件时出错: {e}")

    def load_config(self):
        """读取配置文档"""

        if os.path.exists('config.json'):
            try:
                with open('config.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # ------------------------上号-------------------------------------
                    self.mima_file_path_input.setText(config.get('mimaben_path'))  # 密码路径
                    self.mimaben_path = self.mima_file_path_input.text()  # 密码本路径
                    if self.mimaben_path != '':
                        self.add_items_to_combobox(self.qqnumb)
                    self.huoyankami.setText(config.get('huoyan', ''))  # 火眼卡密
                    if config.get('qq') is not None:
                        self.qqnumb.setCurrentText(config.get('qq'))  # 选择qq号
                    self.zhijbanzhuan.setChecked(config.get('zhixingbanzhuan', False))  # 是否搬砖
                    # ------------------------搬砖-------------------------------------
                    self.ditu.setCurrentText(config.get('tu', ''))
                    self.nandu.setCurrentText(config.get('dengji', ''))  # 搬砖地图等级
                    # ------------------------扫拍-------------------------------------
                    self.name.setText(config.get('wupin_name', ''))
                    self.jiage.setText(config.get('mubiaojiage', ''))
                    self.start_time.setText(config.get('suijianqujian', ''))
                    self.end_time.setText(config.get('suijianqujian2', ''))
                    self.checkbox1.setChecked(config.get('youdanjia', False))
                    self.checkbox2.setChecked(config.get('chushihua', False))
                    # ------------------------其他-------------------------------------
                    self.file_path_input.setText(config.get('wupinjiage_path', ''))
                    self.lianjin_file_path_input.setText(config.get('lianjinshu_path', ''))
            except Exception as e:
                print(f"加载配置文件时出错: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MyWindo = MW()
    thread = Thread(target=MyWindo.start_global_key_listener)
    thread.daemon = True
    thread.start()
    MyWindo.show()
    sys.exit(app.exec_())
