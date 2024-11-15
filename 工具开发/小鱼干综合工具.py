import sys
import time
import threading
from PyQt5.QtCore import QThread, pyqtSignal, QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QStackedLayout, \
    QTextEdit, QLineEdit, QCheckBox
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

        # 右侧页面栏布局，使用堆栈布局方便切换页面
        self.page_layout = QStackedLayout()

        # 创建页面
        self.create_pages()

        # 创建按钮并添加到左侧按钮栏布局
        self.create_buttons()

        # 将按钮栏布局和页面布局添加到主布局
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addLayout(self.page_layout)
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
        self.button_layout.addWidget(self.button_page1)

        self.button_page2 = QPushButton("扫拍", self)
        self.button_page2.clicked.connect(lambda: self.switch_page(1))
        self.button_layout.addWidget(self.button_page2)

        self.button_page3 = QPushButton("其他", self)
        self.button_page3.clicked.connect(lambda: self.switch_page(2))
        self.button_layout.addWidget(self.button_page3)

        # 默认显示第一页
        self.page_layout.setCurrentIndex(0)

    def switch_page(self, index):
        """根据索引切换页面"""
        self.page_layout.setCurrentIndex(index)

    def indesx_1(self):
        """第一页内容"""
        page1_layout_total = QHBoxLayout(self.page1)
        # 第一列布局，包含下拉框和开始按钮
        page1_layout1 = QVBoxLayout(self.page1)
        page1_layout4 = QHBoxLayout(self.page1)
        page1_layout5 = QHBoxLayout(self.page1)
        page1_layout6 = QHBoxLayout(self.page1)
        page1_layout1.addStretch()
        page1_layout4.addStretch()
        combo = QComboBox(self.page1)
        combo.addItem("风暴逆鳞")
        combo.addItem("圣殿")
        combo.addItem("海伯伦")
        page1_layout4.addWidget(combo)
        page1_layout4.addStretch()

        page1_layout4.addStretch()
        combo2 = QComboBox(self.page1)
        combo2.setFixedSize(180, 35)

        combo.setFixedSize(180, 35)
        combo2.addItem("普通")
        combo2.addItem("冒险")
        combo2.addItem("勇士")
        combo2.addItem("王者")
        combo2.addItem("噩梦")
        page1_layout4.addWidget(combo2)
        page1_layout4.addStretch()

        page1_layout5.addStretch()
        start = QPushButton('开始')
        start.clicked.connect(self.run_banzhuan)
        start.setFixedSize(180, 35)
        stop = QPushButton('停止')
        stop.clicked.connect(self.force_stop_qthread)
        stop.setFixedSize(180, 35)

        page1_layout5.addWidget(start)
        page1_layout5.addWidget(stop)
        page1_layout5.addStretch()

        # 为了美观和布局管理，可以添加伸展项使组件居中
        page1_layout1.addLayout(page1_layout4)
        page1_layout1.addStretch()
        page1_layout1.addLayout(page1_layout6)
        page1_layout1.addStretch()
        page1_layout1.addLayout(page1_layout5)
        page1_layout_total.addLayout(page1_layout1)
        for i in range(20):
            page1_layout1.addStretch()

        # 第二列布局，仅包含文本编辑框
        page1_layout2 = QVBoxLayout(self.page1)
        self.edig = edig = QTextEdit(self.page1)
        edig.setReadOnly(True)
        self.set_banzhuan_log('初始化完成')
        edig.setFixedSize(500, 888)  # 设置文本编辑框的固定大小
        page1_layout2.addWidget(edig)
        page1_layout_total.addLayout(page1_layout2)

        # self.page_layout.addWidget(self.page1)

    def indesx_2(self):
        """第二页内容"""
        page1_layout_total = QHBoxLayout(self.page2)
        # 第一列布局，包含下拉框和开始按钮
        page1_layout1 = QVBoxLayout(self.page2)  # 第一列
        page1_layout4 = QHBoxLayout(self.page2)  # 第一行
        page1_layout5 = QHBoxLayout(self.page2)  # 第二行
        page1_layout6 = QHBoxLayout(self.page2)  # 第三行
        page1_layout7 = QHBoxLayout(self.page2)  # 第四行
        page1_layout8 = QHBoxLayout(self.page2)  # 第四行

        # 第一行
        wupinming = QLabel("物品名称:", self.page2)
        page1_layout4.addWidget(wupinming)
        name = QLineEdit(self.page2)
        page1_layout4.addWidget(name)
        wupinming.setFixedSize(110, 35)

        # 第二行
        mubiaojiage = QLabel("目标价格:", self.page2)
        page1_layout5.addWidget(mubiaojiage)
        jiage = QLineEdit(self.page2)
        page1_layout5.addWidget(jiage)
        mubiaojiage.setFixedSize(110, 35)

        # 第三行
        tingzhi = QLabel("扫怕停止:", self.page2)
        page1_layout6.addWidget(tingzhi)
        jiner = QLineEdit(self.page2)
        jiner.setPlaceholderText("默认不自动停止")

        page1_layout6.addWidget(jiner)
        mubiaojiage.setFixedSize(110, 35)

        # 第四行 创建一个点选按钮
        checkbox1 = QCheckBox("是否有单价", self)
        checkbox1.setChecked(True)
        page1_layout7.addWidget(checkbox1)

        checkbox2 = QCheckBox("是否要初始化", self)
        checkbox2.setChecked(True)
        page1_layout7.addWidget(checkbox2)

        #
        start = QPushButton('扫拍-开始/Home')
        start.clicked.connect(self.run_banzhuan)
        start.setFixedSize(180, 66)
        stop = QPushButton('搓药')
        stop.clicked.connect(self.force_stop_qthread)
        stop.setFixedSize(180, 66)

        page1_layout8.addWidget(start)
        page1_layout8.addWidget(stop)

        # 为了美观和布局管理，可以添加伸展项使组件居中
        page1_layout1.addStretch()
        page1_layout1.addLayout(page1_layout4)
        page1_layout1.addStretch()
        page1_layout1.addLayout(page1_layout5)
        page1_layout1.addStretch()
        page1_layout1.addLayout(page1_layout6)
        page1_layout1.addStretch()
        page1_layout1.addLayout(page1_layout7)
        page1_layout1.addStretch()
        page1_layout1.addLayout(page1_layout8)
        page1_layout1.addStretch()
        page1_layout_total.addLayout(page1_layout1)
        for i in range(18):
            page1_layout1.addStretch()

        # 第二列布局，仅包含文本编辑框
        page1_layout2 = QVBoxLayout(self.page2)
        self.edig = edig = QTextEdit(self.page2)
        edig.setReadOnly(True)
        # self.set_banzhuan_log('初始化完成')
        edig.setFixedSize(500, 888)  # 设置文本编辑框的固定大小
        page1_layout2.addWidget(edig)
        page1_layout_total.addLayout(page1_layout2)

    def indesx_3(self):
        """第二页内容"""
        page1_layout_total = QHBoxLayout(self.page3)
        # 第一列布局，包含下拉框和开始按钮
        page1_layout1 = QVBoxLayout(self.page3)  # 第一列
        page1_layout4 = QHBoxLayout(self.page3)  # 第一行
        page1_layout5 = QHBoxLayout(self.page3)  # 第二行
        # page1_layout6 = QHBoxLayout(self.page3)  # 第三行
        # page1_layout7 = QHBoxLayout(self.page3)  # 第四行
        # page1_layout8 = QHBoxLayout(self.page3)  # 第四行

        # 第一行
        wupinming = QLabel("CF速点宏:", self.page3)
        page1_layout4.addWidget(wupinming)
        start = QPushButton("开始/home", self.page3)
        page1_layout4.addWidget(start)
        wupinming.setFixedSize(150, 35)

        # 当按钮被点击时触发的动作
        start.clicked.connect(self.right_click)
        page1_layout4.addStretch()

        # 第二行
        youjian = QLabel("CF连续右键:", self.page3)
        page1_layout5.addWidget(youjian)
        start_youjiao = QPushButton("开始/end", self.page3)
        page1_layout5.addWidget(start_youjiao)
        youjian.setFixedSize(150, 35)
        # 当按钮被点击时触发的动作
        start_youjiao.clicked.connect(self.left_click)
        page1_layout5.addStretch()


        # 第三行
        # tingzhi = QLabel("扫怕停止:", self.page3)
        # page1_layout6.addWidget(tingzhi)
        # jiner = QLineEdit(self.page3)
        # jiner.setPlaceholderText("默认不自动停止")
        #
        # page1_layout6.addWidget(jiner)
        # mubiaojiage.setFixedSize(110, 35)
        #
        # # 第四行 创建一个点选按钮
        # checkbox1 = QCheckBox("是否有单价", self)
        # checkbox1.setChecked(True)
        # page1_layout7.addWidget(checkbox1)
        #
        # checkbox2 = QCheckBox("是否要初始化", self)
        # checkbox2.setChecked(True)
        # page1_layout7.addWidget(checkbox2)
        #
        # #
        # start = QPushButton('扫拍-开始/Home')
        # start.clicked.connect(self.run_banzhuan)
        # start.setFixedSize(180, 66)
        # stop = QPushButton('搓药')
        # stop.clicked.connect(self.force_stop_qthread)
        # stop.setFixedSize(180, 66)
        #
        # page1_layout8.addWidget(start)
        # page1_layout8.addWidget(stop)

        # 为了美观和布局管理，可以添加伸展项使组件居中
        page1_layout1.addStretch()
        page1_layout1.addLayout(page1_layout4)
        page1_layout1.addStretch()
        page1_layout1.addLayout(page1_layout5)
        page1_layout1.addStretch()
        # page1_layout1.addLayout(page1_layout6)
        # page1_layout1.addStretch()
        # page1_layout1.addLayout(page1_layout7)
        # page1_layout1.addStretch()
        # page1_layout1.addLayout(page1_layout8)
        # page1_layout1.addStretch()
        page1_layout_total.addLayout(page1_layout1)
        for i in range(18):
            page1_layout1.addStretch()

        # # 第二列布局，仅包含文本编辑框
        # page1_layout2 = QVBoxLayout(self.page3)
        # self.edig = edig = QTextEdit(self.page3)
        # edig.setReadOnly(True)
        # # self.set_banzhuan_log('初始化完成')
        # edig.setFixedSize(500, 888)  # 设置文本编辑框的固定大小
        # page1_layout2.addWidget(edig)
        # page1_layout_total.addLayout(page1_layout2)

    def right_click(self):
        """速点"""
        pass

    def left_click(self):
        """右键速点"""
        pass


    def set_banzhuan_log(self, data):
        "板砖页面的log输出在 log框里"
        self.edig.insertPlainText(f"{data}\n")

        cursor = self.edig.textCursor()
        # cursor.movePosition(cursor.End)
        self.edig.setTextCursor(cursor)

    def run_banzhuan(self):
        """搬砖代码"""
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
