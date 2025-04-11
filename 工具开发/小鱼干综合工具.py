import sys
import time
import threading
from PyQt5.QtCore import QThread, pyqtSignal, QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QStackedLayout, \
    QTextEdit, QLineEdit, QCheckBox, QFrame, QFileDialog
from PyQt5.QtWidgets import QComboBox
from pynput import keyboard


class ErrorHandler(QObject):
    sigException = pyqtSignal(object, object, str)

    def __init__(self):
        super().__init__()
        sys.excepthook = self.handleException

    @pyqtSlot(object, object, str)
    def handleException(self, exc_type, exc_value, traceback_str):
        print(f"Caught exception: {exc_type} - {exc_value}\n{traceback_str}")


error_handler = ErrorHandler()

app2 = QApplication(sys.argv)


class Worker(QThread):
    finished = pyqtSignal()  # 自定义信号，用于通知工作完成

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName('testID')

    def run(self):
        print("开始执行耗时操作...")
        for i in range(10):
            window.set_banzhuan_log("你干嘛~，哎呦~")
            time.sleep(1)  # 模拟耗时操作

        print("耗时操作结束")
        self.finished.emit()  # 发送信号表示任务完成


class MultiPageWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = Worker()
        self.setWindowTitle("小鱼干综合工具")
        self.setGeometry(1140, 50, 1100, 1000)  # 初始化窗口大小，
        # 主布局，水平布局，包含左侧按钮栏和右侧页面栏
        self.main_layout = QHBoxLayout(self)

        # 左侧按钮栏布局
        self.button_layout = QVBoxLayout()
        self.log_layout = QVBoxLayout()
        # 右侧页面栏布局，使用堆栈布局方便切换页面
        self.page_layout = QStackedLayout()

        # 创建切换页面
        self.create_pages()

        # 创建按钮页面
        self.create_buttons()

        # 创建log页面
        self.create_log()

        # 将按钮栏布局和页面布局添加到主布局
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addLayout(self.page_layout)
        self.main_layout.addLayout(self.log_layout)

        # # 启动全局按键监听
        # self.start_global_key_listener()
    def create_pages(self):
        self.page1 = QWidget()
        self.page1.setObjectName("Page1")
        self.page1.setStyleSheet("""
            #Page1 {
                border-left: 2px solid black; /* 仅设置左侧边框宽度为2px，样式为实线，颜色为黑色 */
                padding-left: 5px; /* 可选，仅设置左侧内边距，让边框和内容之间有一定的间隔 */
            }
        """)
        self.indesx_1()
        self.page_layout.addWidget(self.page1)
        ######################################################################################################################
        self.page2 = QWidget()
        self.page2.setObjectName("Page2")
        self.page2.setStyleSheet("""
            #Page2 {
                border-left: 2px solid black; /* 仅设置左侧边框宽度为2px，样式为实线，颜色为黑色 */
                padding-left: 5px; /* 可选，仅设置左侧内边距，让边框和内容之间有一定的间隔 */
            }
        """)
        self.indesx_2()
        # self.label_page2 = QLabel("这是第二页内容", self.page2)
        self.page_layout.addWidget(self.page2)
        ######################################################################################################################

        self.page3 = QWidget()
        self.page3.setObjectName("Page2")
        self.page3.setStyleSheet("""
            #Page2 {
                border-left: 2px solid black; /* 仅设置左侧边框宽度为2px，样式为实线，颜色为黑色 */
                padding-left: 5px; /* 可选，仅设置左侧内边距，让边框和内容之间有一定的间隔 */
            }
        """)
        self.indesx_3()
        self.page_layout.addWidget(self.page3)

    def create_buttons(self):
        self.button_page1 = QPushButton("搬砖", self)
        self.button_page1.clicked.connect(lambda: self.switch_page(0))
        self.button_page1.setStyleSheet("QPushButton{background-color:rgb(206, 202, "
                                        "255);border:none;height:44px;width: 180px;border-radius:9px;}QPushButton::hover{"
                                        "background-color:rgb(155, 146, "
                                        "255);border:none;height:24px;border-radius:9px;}")

        self.button_layout.addWidget(self.button_page1)

        self.button_page2 = QPushButton("扫拍", self)
        self.button_page2.clicked.connect(lambda: self.switch_page(1))
        self.button_page2.setStyleSheet("QPushButton{background-color:rgb(206, 202, "
                                        "255);border:none;height:44px;width: 180px;border-radius:9px;}QPushButton::hover{"
                                        "background-color:rgb(155, 146, "
                                        "255);border:none;height:24px;border-radius:9px;}")

        self.button_layout.addWidget(self.button_page2)

        self.button_page3 = QPushButton("其他", self)
        self.button_page3.setStyleSheet("QPushButton{background-color:rgb(206, 202, 255);border:none;height:44px; "
                                        "width: 180px;border-radius:9px;}QPushButton::hover{background-color:rgb(155, "
                                        "146, 255);border:none;height:54px;border-radius:9px;}")
        self.button_page3.clicked.connect(lambda: self.switch_page(2))
        self.button_layout.addWidget(self.button_page3)
        self.button_layout.addStretch()
        # 默认显示第一页
        self.page_layout.setCurrentIndex(0)

    def create_log(self):
        """创建log页面"""
        # 第二列布局，仅包含文本编辑框
        page1_layout2 = QVBoxLayout(self.page1)
        self.edig = edig = QTextEdit(self.page1)
        edig.setReadOnly(True)
        self.set_banzhuan_log('初始化完成')
        edig.setFixedSize(500, 888)  # 设置文本编辑框的固定大小
        page1_layout2.addWidget(edig)
        self.log_layout.addLayout(page1_layout2)



    def switch_page(self, index):
        """根据索引切换页面"""
        self.page_layout.setCurrentIndex(index)


    def indesx_1(self):
        """第一页内容"""
        page1_layout_total = QHBoxLayout(self.page1)
        # 第一列布局，包含下拉框和开始按钮
        page1_layout0 = QVBoxLayout(self.page1)  # 创建一个盒子
        page1_layout1 = QHBoxLayout(self.page1)  # 第一行
        page1_layout2 = QHBoxLayout(self.page1)  # 第二行
        page1_layout6 = QHBoxLayout(self.page1)  # 第三行
        self.ditu = QComboBox(self.page1)
        self.ditu.addItem("风暴逆鳞")
        page1_layout1.addWidget(self.ditu)
        self.nandu = QComboBox(self.page1)
        self.nandu.setFixedSize(200, 50)

        self.ditu.setFixedSize(200, 50)
        self.nandu.addItem("普通")
        self.nandu.addItem("冒险")
        self.nandu.addItem("勇士")
        self.nandu.addItem("王者")
        self.nandu.addItem("噩梦")
        page1_layout1.addWidget(self.nandu)
        self.banzhuan_start = QPushButton('开始')
        self.banzhuan_start.setStyleSheet("""
QPushButton {
    background-color: rgb(34, 40, 49);
    border: 2px solid rgb(0, 173, 181);
    height: 44px;
    width: 180px;
    border-radius: 30px;
    color: rgb(0, 173, 181);
    font-size: 30px;
    font-weight: bold;
}
QPushButton::hover {
    background-color: rgb(57, 62, 70);
    border: 2px solid rgb(0, 200, 208);
    height: 44px;
    border-radius: 10px;
    color: rgb(0, 200, 208);
}
QPushButton::pressed {
    background-color: rgb(23, 27, 33);
    border: 2px solid rgb(0, 120, 126);
    height: 44px;
    border-radius: 10px;
    color: rgb(0, 120, 126);
}
""")
        self.banzhuan_start.setFixedSize(200, 100)
        self.banzhuan_stop = QPushButton('停止/home')
        self.banzhuan_stop.setFixedSize(200, 100)

        page1_layout2.addWidget(self.banzhuan_start)
        page1_layout2.addWidget(self.banzhuan_stop)

        # 为了美观和布局管理，可以添加伸展项使组件居中
        page1_layout0.addLayout(page1_layout1)
        page1_layout0.addLayout(page1_layout6)
        page1_layout0.addLayout(page1_layout2)
        page1_layout_total.addLayout(page1_layout0)
        page1_layout0.addStretch()

    def indesx_2(self):
        """第二页内容"""
        page1_layout_total = QHBoxLayout(self.page2)
        # 第一列布局，包含下拉框和开始按钮
        page1_layout0 = QVBoxLayout(self.page2)  # 第一列  # 创建一个空间，所有元素都加入这个空间中
        page1_layout1 = QHBoxLayout(self.page2)  # 第一行  # 物品名称
        page1_layout2 = QHBoxLayout(self.page2)  # 第二行  # 目标价格
        page1_layout3 = QHBoxLayout(self.page2)  # 第三行  # 随机间隔
        page1_layout4 = QHBoxLayout(self.page2)  # 第四行  # 扫拍停止
        page1_layout5 = QHBoxLayout(self.page2)  # 第五行  # 是否有单价，是否需要初始化
        page1_layout6 = QHBoxLayout(self.page2)  # 第六行  # 开始

        # 第一行
        wupinming = QLabel("物品名称:", self.page2)
        page1_layout1.addWidget(wupinming)
        self.name = QLineEdit(self.page2)
        page1_layout1.addWidget(self.name)
        wupinming.setFixedSize(110, 35)
        # 第二行
        mubiaojiage = QLabel("目标价格:", self.page2)
        page1_layout2.addWidget(mubiaojiage)
        self.jiage = QLineEdit(self.page2)
        page1_layout2.addWidget(self.jiage)
        mubiaojiage.setFixedSize(110, 35)

        # 第三行
        mubiaojiage = QLabel("间隔时间:", self.page2)
        page1_layout3.addWidget(mubiaojiage)
        self.start_time = QLineEdit(self.page2)
        page1_layout3.addWidget(self.start_time)
        lianjie = QLabel("-", self.page2)
        page1_layout3.addWidget(lianjie)
        self.end_time = QLineEdit(self.page2)
        page1_layout3.addWidget(self.end_time)

        # # 第三行
        # tingzhi = QLabel("扫怕停止:", self.page2)
        # page1_layout4.addWidget(tingzhi)
        # jiner = QLineEdit(self.page2)
        # jiner.setPlaceholderText("默认不自动停止")
        # page1_layout4.addWidget(jiner)
        # mubiaojiage.setFixedSize(110, 35)

        # 第四行 创建一个点选按钮
        self.checkbox1 = QCheckBox("是否有单价", self)
        page1_layout5.addWidget(self.checkbox1)
        self.checkbox2 = QCheckBox("是否要初始化", self)
        page1_layout5.addWidget(self.checkbox2)

        # 第五行 创建一个点选按钮
        self.start = QPushButton('扫拍-开始/Home')
        self.start.setFixedSize(200, 66)
        self.stop = QPushButton('搓药')
        self.stop.setFixedSize(200, 66)

        page1_layout6.addWidget(self.start)
        page1_layout6.addWidget(self.stop)

        # 为了美观和布局管理，可以添加伸展项使组件居中
        page1_layout0.addLayout(page1_layout1)
        page1_layout0.addLayout(page1_layout2)
        page1_layout0.addLayout(page1_layout3)
        page1_layout0.addLayout(page1_layout4)
        page1_layout0.addLayout(page1_layout5)
        page1_layout0.addLayout(page1_layout6)
        page1_layout_total.addLayout(page1_layout0)
        page1_layout0.addStretch()

    def indesx_3(self):
        """第二页内容"""
        page1_layout_total = QHBoxLayout(self.page3)
        # 第一列布局，包含下拉框和开始按钮
        page1_layout0 = QVBoxLayout(self.page3)  #
        page1_layout1 = QHBoxLayout(self.page3)  # 第一行
        page1_layout2 = QHBoxLayout(self.page3)  # 第二行
        page1_layout3 = QHBoxLayout(self.page3)  # 第三行
        page1_layout4 = QHBoxLayout(self.page3)  # 第四行

        # 第一行
        wupinming = QLabel("兑换工会卡:", self.page3)
        page1_layout1.addWidget(wupinming)
        self.gonghuika = QPushButton("开始", self.page3)
        page1_layout1.addWidget(self.gonghuika)
        # wupinming.setFixedSize(200, 35)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)  # 水平分割线
        separator.setLineWidth(2)

        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)  # 水平分割线
        separator2.setLineWidth(2)
        separator3 = QFrame()
        separator3.setFrameShape(QFrame.HLine)  # 水平分割线
        separator3.setLineWidth(2)



        # separator.setFrameShadow(QFrame.Sunken)
        # 第二行
        youjian = QLabel("兑换黄龙白玉宝珠:", self.page3)
        page1_layout2.addWidget(youjian)
        self.duihuanbaiyu = QPushButton("开始", self.page3)
        page1_layout2.addWidget(self.duihuanbaiyu)
        # youjian.setFixedSize(200, 35)

        # 第三行
        shangpjiage = QLabel("商品价格记录:", self.page3)
        # shangpjiage.setFixedSize(200, 35)
        page1_layout3.addWidget(shangpjiage)
        self.jilushangpin = QPushButton("开始", self.page3)
        page1_layout3.addWidget(self.jilushangpin)
        # youjian.setFixedSize(200, 35)

        select_file_button = QPushButton("选择文件", self)
        # select_file_button.setFixedSize(100, 35)
        select_file_button.clicked.connect(self.select_file)
        page1_layout4.addWidget(select_file_button)
        self.file_path_input = QLineEdit(self)
        # select_file_button.setFixedSize(100, 35)
        self.file_path_input.setReadOnly(True)
        page1_layout4.addWidget(self.file_path_input)

        page1_layout0.addLayout(page1_layout1)
        page1_layout0.addWidget(separator)
        page1_layout0.addLayout(page1_layout2)
        page1_layout0.addWidget(separator2)
        page1_layout0.addLayout(page1_layout3)
        page1_layout0.addLayout(page1_layout4)
        page1_layout0.addWidget(separator3)


        page1_layout_total.addLayout(page1_layout0)
        page1_layout0.addStretch()
        page1_layout_total.addStretch()

    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "选择文件", "", "所有文件 (*.*)")
        if file_path:
            self.file_path_input.setText(file_path)

    def set_banzhuan_log(self, data):
        "板砖页面的log输出在 log框里"
        self.edig.insertPlainText(f"{data}\n")

        cursor = self.edig.textCursor()
        # cursor.movePosition(cursor.End)
        self.edig.setTextCursor(cursor)

    def run_banzhuan(self):
        """搬砖代码"""
        name = self.name.text()
        print(name)
        # self.worker = Worker()
        # self.set_banzhuan_log('你干嘛~ ，哎呦~')
        self.worker.start()  # 在单独的线程中开始执行耗时任务

    def force_stop_qthread(self):
        self.worker.dumpObjectInfo()
        return
        # 注意：以下操作涉及私有属性，违反了Qt的使用原则，强烈不推荐！
        import ctypes
        import os
        # os.system('tasklist')
        import psutil
        for proc in psutil.process_iter(['threads']):
            if proc.pid == os.getpid():  # 只检查当前进程
                for x in proc.threads():
                    print(x)
        return None

    def start_global_key_listener(self):
        print(2)
        with keyboard.Listener(on_press=self.on_press) as listener:
            self.listener = listener
            self.listener.join()
            self.page_layout.currentIndex()

    def on_press(self, key):
        try:
            if key == keyboard.Key.home:
                print('home')
                # 你可以在这里添加其他操作
            if key == keyboard.Key.end:
                print('end')
                # 你可以在这里添加其他操作

        except AttributeError:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MultiPageWindow()
    # print = window.set_banzhuan_log
    window.show()
    # 在主线程中启动键盘监听器
    from threading import Thread
    thread = Thread(target=window.start_global_key_listener)
    thread.daemon = True
    thread.start()

    sys.exit(app.exec_())
