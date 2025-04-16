import sys
import time
import threading
from PyQt5.QtCore import QThread, pyqtSignal, QObject, pyqtSlot, Qt
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


class MultiPageWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.button_style = """
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
                    color: rgb(206, 249, 6); /*鼠标悬停的颜色*/
                    border: 2px solid rgb(206, 249, 6);  /* 添加边框，宽度为 2px，颜色为黑色 */
                }
                QPushButton::pressed {
                    background-color: rgb(23, 27, 33);
                    border: 2px solid rgb(0, 120, 126);
                    height: 44px;
                    border-radius: 10px;
                    color: rgb(0, 120, 126);
                }
                """
        self.setWindowTitle("小鱼干综合工具")
        self.setStyleSheet("background-color: #222222;")  # 这里使用十六进制颜色代码，你可以根据需要修改
        self.setGeometry(1140, 0, 1100, 1000)  # 初始化窗口大小，
        # self.setFixedSize(1100, 1000)  # 设置窗口的固定大小，宽度为 1100，高度为 1000
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 窗口始终置顶

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
                border-left: 2px solid rgb(255, 255, 128);  仅设置左侧边框宽度为2px，样式为实线，颜色为黑色 */
                padding-left: 5px; /* 可选，仅设置左侧内边距，让边框和内容之间有一定的间隔 */
            }
        """)
        self.indesx_1()
        self.page_layout.addWidget(self.page1)
        self.page2 = QWidget()
        self.page2.setObjectName("Page2")
        self.page2.setStyleSheet("""
            #Page2 {
                border-left: 2px solid rgb(255, 255, 128);  仅设置左侧边框宽度为2px，样式为实线，颜色为黑色 */
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
                border-left: 2px solid rgb(255, 255, 128);  仅设置左侧边框宽度为2px，样式为实线，颜色为黑色 */
                padding-left: 5px; /* 可选，仅设置左侧内边距，让边框和内容之间有一定的间隔 */
            }
        """)
        self.indesx_3()

        self.page0 = QWidget()
        self.page0.setObjectName("Page4")
        self.page0.setStyleSheet("""
            #Page4 {
                border-left: 2px solid rgb(255, 255, 128);  仅设置左侧边框宽度为2px，样式为实线，颜色为黑色 */
                padding-left: 5px; /* 可选，仅设置左侧内边距，让边框和内容之间有一定的间隔 */
            }
        """)
        self.indesx_0()
        self.page_layout.addWidget(self.page3)

        self.page_layout.addWidget(self.page0)


    def create_buttons(self):
        self.button_page0 = QPushButton("上号", self)
        self.button_page0.clicked.connect(lambda: self.switch_page(3))
        self.button_page0.setCheckable(True)
        style = """
                   QPushButton {
                    background-color: #222831;
                    border: 2px solid #00ADB5;
                    height: 44px;
                    min-width: 180px;
                    color: #EEEEEE;
                    font-size: 30px;
                    font-weight: bold;
                    border-radius: 10px;
                    padding: 5px;
                }
                QPushButton:hover {
                    color: rgb(206, 249, 6); /*鼠标悬停的颜色*/
                    border: 2px solid rgb(206, 249, 6);  /* 添加边框，宽度为 2px，颜色为黑色 */
                }
                QPushButton:pressed {
                    background-color: #393E46;
                    border: 2px solid #00ADB5;
                    color: #00ADB5;
                }
                QPushButton:checked {
                    color: #FFD369;
                    border-color: #FFD369;
                }
                """

        self.button_page0.setStyleSheet(style)

        self.button_layout.addWidget(self.button_page0)
        #############################################
        self.button_page1 = QPushButton("搬砖", self)
        self.button_page1.clicked.connect(lambda: self.switch_page(0))
        self.button_page1.setCheckable(True)

        self.button_page1.setStyleSheet(style)

        self.button_layout.addWidget(self.button_page1)

        self.button_page2 = QPushButton("扫拍", self)
        self.button_page2.clicked.connect(lambda: self.switch_page(1))
        self.button_page2.setStyleSheet(style)
        self.button_page2.setCheckable(True)
        self.button_layout.addWidget(self.button_page2)

        self.button_page3 = QPushButton("其他", self)
        self.button_page3.setStyleSheet(style)
        self.button_page3.clicked.connect(lambda: self.switch_page(2))
        self.button_page3.setCheckable(True)
        self.button_layout.addWidget(self.button_page3)
        self.button_layout.addStretch()
        # 默认显示第一页
        self.page_layout.setCurrentIndex(3)
        self.button_page0.setChecked(True)

    def create_log(self):
        """创建log页面"""
        # 第二列布局，仅包含文本编辑框
        page1_layout2 = QVBoxLayout(self.page1)
        self.edig = edig = QTextEdit(self.page1)
        textedit_style = """
                QTextEdit {
                    background-color: rgb(0, 30, 49);  /*背景色*/
                    
                    border-radius: 10px;
                    color: rgb(0, 200, 208); 
                    font-size: 30px;
                    font-weight: bold;
                    padding: 15px;
                }
                QTextEdit::hover {
                    color: rgb(206, 249, 6); /*鼠标悬停的颜色*/
                    border: 2px solid rgb(206, 249, 6);  /* 添加边框，宽度为 2px，颜色为黑色 */
                }
                QTextEdit QScrollBar:vertical {
                    background: rgb(34, 40, 49);
                    width: 15px;
                    margin: 15px 3px 15px 3px;
                    border: 1px solid rgb(0, 173, 181);
                    border-radius: 10px;
                }
                QTextEdit QScrollBar::handle:vertical {
                    background-color: rgb(0, 173, 181);
                    min-height: 5px;
                    border-radius: 4px;
                }
                QTextEdit QScrollBar::add-line:vertical {
                    border: none;
                    background: rgb(34, 40, 49);
                    height: 15px;
                    subcontrol-position: bottom;
                    subcontrol-origin: margin;
                }
                QTextEdit QScrollBar::add-line:vertical:hover {
                    background: rgb(40, 46, 55);
                }
                QTextEdit QScrollBar::add-line:vertical:pressed {
                    background: rgb(0, 173, 181);
                }
                QTextEdit QScrollBar::sub-line:vertical {
                    border: none;
                    background: rgb(34, 40, 49);
                    height: 15px;
                    subcontrol-position: top;
                    subcontrol-origin: margin;
                }
                QTextEdit QScrollBar::sub-line:vertical:hover {
                    background: rgb(40, 46, 55);
                }
                QTextEdit QScrollBar::sub-line:vertical:pressed {
                    background: rgb(0, 173, 181);
                }
                QTextEdit QScrollBar::add-page:vertical, QTextEdit QScrollBar::sub-page:vertical {
                    background: none;
                }
            """
        self.edig.setStyleSheet(textedit_style)
        edig.setReadOnly(True)
        self.set_banzhuan_log('初始化完成')
        edig.setFixedWidth(500)  # 只固定宽度
        page1_layout2.addWidget(edig)
        self.log_layout.addLayout(page1_layout2)

    def switch_page(self, index):
        """根据索引切换页面"""
        self.button_page0.setChecked(False)
        self.button_page1.setChecked(False)
        self.button_page2.setChecked(False)
        self.button_page3.setChecked(False)
        if index == 0:
            self.button_page1.setChecked(True)
        elif index == 1:
            self.button_page2.setChecked(True)
        elif index == 2:
            self.button_page3.setChecked(True)
        elif index == 3:
            self.button_page0.setChecked(True)

        self.page_layout.setCurrentIndex(index)
    def add_items_to_combobox(self, combobox):
        """
        封装的函数，用于向 QComboBox 中添加列表项
        :param combobox: QComboBox 对象
        :param item_list: 要添加的列表项列表
        """
        with open(self.mima_file_path_input.text(), 'r', encoding='utf-8') as fp:
            item_list = [line.strip() for line in fp.readlines()]
            self.qq_json = {}
            qq_list =[]
            for item in item_list:
                qq_pwd = item.split(',')
                self.qq_json[qq_pwd[0]] = qq_pwd[1]
                qq_list.append(qq_pwd[0])
            combobox.addItems(qq_list)


    def indesx_0(self):
        """账号登录"""
        page0_layout_total = QHBoxLayout(self.page0)
        page0_layout0 = QVBoxLayout(self.page0)  # 创建一个盒子
        page0_layout1 = QHBoxLayout(self.page0)  # 第一行
        page0_layout2 = QHBoxLayout(self.page0)  # 第二行
        page0_layout3 = QHBoxLayout(self.page0)  # 第三行
        page0_layout4 = QHBoxLayout(self.page0)  # 第三行


        self.mimaben = QPushButton('选择密码本')
        self.mimaben.setStyleSheet(self.button_style)
        self.mimaben.clicked.connect(self.huqumima)

        self.mima_file_path_input = QLineEdit(self)
        self.mima_file_path_input.setStyleSheet(self.lineedit_style)
        self.mima_file_path_input.setReadOnly(True)

        self.huoyan = QLabel('火眼答题卡密:')
        self.huoyan.setStyleSheet(self.label_style)
        self.huoyankami = QLineEdit(self)
        self.huoyankami.setStyleSheet(self.lineedit_style)

        self.qqnumb = QComboBox(self.page0)
        self.qqnumb.setStyleSheet(self.style)

        self.zhijbanzhuan = QCheckBox("直接搬砖")
        self.zhijbanzhuan.setStyleSheet(self.checkbox_style)

        self.shanghao = QPushButton('上号')
        self.shanghao.setStyleSheet(self.button_style)
        self.shanghao.setFixedSize(400, 100)
        page0_layout1.addWidget(self.mima_file_path_input)
        page0_layout1.addWidget(self.mimaben)
        page0_layout2.addWidget(self.huoyan)
        page0_layout2.addWidget(self.huoyankami)
        page0_layout3.addWidget(self.qqnumb)
        page0_layout3.addWidget(self.zhijbanzhuan)

        page0_layout4.addWidget(self.shanghao)

        page0_layout0.addLayout(page0_layout1)
        page0_layout0.addLayout(page0_layout2)
        page0_layout0.addLayout(page0_layout3)
        page0_layout0.addLayout(page0_layout4)

        page0_layout0.addStretch()
        page0_layout_total.addLayout(page0_layout0)

    def indesx_1(self):
        """第一页内容"""
        page1_layout_total = QHBoxLayout(self.page1)
        # 第一列布局，包含下拉框和开始按钮
        page1_layout0 = QVBoxLayout(self.page1)  # 创建一个盒子
        page1_layout1 = QHBoxLayout(self.page1)  # 第一行
        page1_layout2 = QHBoxLayout(self.page1)  # 第二行
        page1_layout6 = QHBoxLayout(self.page1)  # 第三行
        self.ditu = QComboBox(self.page1)
        self.style = style = """
        QComboBox {
            background-color: rgb(34, 40, 49);
            border: 2px solid rgb(0, 173, 181);
            height: 44px;
            min-width: 180px;
            border-radius: 30px;
            color: rgb(0, 173, 181);
            font-size: 30px;
            font-weight: bold;
            padding-left: 15px;
        }
        QComboBox::drop-down {
            width: 30px;
        }
        QComboBox::hover {
                                color: rgb(206, 249, 6); /*鼠标悬停的颜色*/
                    border: 2px solid rgb(206, 249, 6);  /* 添加边框，宽度为 2px，颜色为黑色 */
        }
        QComboBox QAbstractItemView {
            background-color: rgb(34, 40, 49);
            border: 2px solid rgb(0, 173, 181);
            color: rgb(0, 173, 181);
            selection-background-color: rgb(0, 173, 181);
            selection-color: white;
        }
        """
        self.ditu.setStyleSheet(style)
        self.ditu.addItem("风暴逆鳞")
        page1_layout1.addWidget(self.ditu)
        self.nandu = QComboBox(self.page1)
        self.nandu.setStyleSheet(style)
        self.nandu.setFixedSize(200, 50)

        self.ditu.setFixedSize(200, 50)
        self.nandu.addItem("普通")
        self.nandu.addItem("冒险")
        self.nandu.addItem("勇士")
        self.nandu.addItem("王者")
        self.nandu.addItem("噩梦")
        page1_layout1.addWidget(self.nandu)
        self.banzhuan_start = QPushButton('开始')

        self.banzhuan_start.setStyleSheet(self.button_style)
        self.banzhuan_start.setFixedSize(200, 100)
        self.banzhuan_stop = QPushButton('停止/home')
        self.banzhuan_stop.setStyleSheet(self.button_style)

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
        self.label_style = """
            QLabel {
                color: rgb(250, 115, 49);
                font-weight: bold;
                text-align: center;
                font-size: 23px; /* 这里可以修改字体大小，单位可以是px、pt等 */

            }
        """
        self.lineedit_style = """
                QLineEdit, QComboBox {
                background-color: #222831;
                border: 2px solid #00ADB5;
                color: #EEEEEE;
                font-size: 20px;
                font-weight: bold;
                border-radius: 15px;
                padding: 5px 15px;
                min-height: 40px;
            }
            QLineEdit:hover, QComboBox:hover {
                border-color: #00D8D8;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #FFD369;
            }
            QComboBox QAbstractItemView {
                background-color: #222831;
                border: 2px solid #00ADB5;
                color: #EEEEEE;
                selection-background-color: #00ADB5;
                selection-color: white;
            }
        """

        self.checkbox_style = checkbox_style = """
                    QCheckBox {
                    color: rgb(250, 115, 49);
                    font-weight: bold;
                    text-align: center;
                    spacing: 23px;
                    }
                    QCheckBox::indicator {
                        width: 20px;
                        height: 20px;
                        border: 2px solid #00ADB5;
                        border-radius: 23px;
                    }
                    QCheckBox::indicator:checked {
                        background-color: #00ADB5;
                    }
            

                    """

        wupinming = QLabel("物品名称:", self.page2)
        wupinming.setStyleSheet(self.label_style)
        page1_layout1.addWidget(wupinming)
        self.name = QLineEdit(self.page2)
        self.name.setStyleSheet(self.lineedit_style)
        page1_layout1.addWidget(self.name)
        wupinming.setFixedSize(110, 35)
        # 第二行
        mubiaojiage = QLabel("目标价格:", self.page2)
        mubiaojiage.setStyleSheet(self.label_style)
        page1_layout2.addWidget(mubiaojiage)
        self.jiage = QLineEdit(self.page2)
        self.jiage.setStyleSheet(self.lineedit_style)
        page1_layout2.addWidget(self.jiage)
        mubiaojiage.setFixedSize(110, 35)

        # 第三行
        mubiaojiage = QLabel("间隔时间:", self.page2)
        mubiaojiage.setStyleSheet(self.label_style)
        page1_layout3.addWidget(mubiaojiage)
        self.start_time = QLineEdit(self.page2)
        self.start_time.setStyleSheet(self.lineedit_style)
        page1_layout3.addWidget(self.start_time)
        lianjie = QLabel("-", self.page2)
        lianjie.setStyleSheet(self.label_style)
        page1_layout3.addWidget(lianjie)
        self.end_time = QLineEdit(self.page2)
        self.end_time.setStyleSheet(self.lineedit_style)
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
        self.checkbox1.setStyleSheet(checkbox_style)
        page1_layout5.addWidget(self.checkbox1)
        self.checkbox2 = QCheckBox("是否要初始化", self)
        self.checkbox2.setStyleSheet(checkbox_style)
        page1_layout5.addWidget(self.checkbox2)

        # 第五行 创建一个点选按钮
        self.start = QPushButton('开始/Home')
        self.start.setStyleSheet(self.button_style)
        self.start.setFixedSize(200, 100)
        self.stop = QPushButton('搓药')
        self.stop.setFixedSize(200, 100)
        self.stop.setStyleSheet(self.button_style)

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
        page1_layout5 = QHBoxLayout(self.page3)  # 第四行
        page1_layout6 = QHBoxLayout(self.page3)  # 第四行
        # 第一行
        wupinming = QLabel("兑换工会卡片:", self.page3)
        wupinming.setStyleSheet(self.label_style)
        page1_layout1.addWidget(wupinming)
        self.gonghuika = QPushButton("开始", self.page3)
        self.gonghuika.setStyleSheet(self.button_style + "QPushButton {border-radius: 10px;}")
        page1_layout1.addWidget(self.gonghuika)
        # wupinming.setFixedSize(200, 35)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)  # 水平分割线
        separator.setLineWidth(2)
        separator.setStyleSheet("color: rgb(255,255, 128);")  # 这里设置为红色，你可以根据需要修改颜色

        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)  # 水平分割线
        separator2.setLineWidth(2)
        separator2.setStyleSheet("color: rgb(255,255, 128);")  # 这里设置为红色，你可以根据需要修改颜色

        separator3 = QFrame()
        separator3.setFrameShape(QFrame.HLine)  # 水平分割线
        separator3.setLineWidth(2)
        separator3.setStyleSheet("color: rgb(255,255, 128);")  # 这里设置为红色，你可以根据需要修改颜色


        # separator.setFrameShadow(QFrame.Sunken)
        # 第二行
        youjian = QLabel("兑换黄龙白玉宝珠:", self.page3)
        youjian.setStyleSheet(self.label_style)
        page1_layout2.addWidget(youjian)
        self.duihuanbaiyu = QPushButton("开始", self.page3)
        self.duihuanbaiyu.setStyleSheet(self.button_style + "QPushButton {border-radius: 10px;}")
        page1_layout2.addWidget(self.duihuanbaiyu)
        # youjian.setFixedSize(200, 35)

        # 第三行
        shangpjiage = QLabel("商品价格记录:", self.page3)
        shangpjiage.setStyleSheet(self.label_style)
        page1_layout3.addWidget(shangpjiage)
        self.jilushangpin = QPushButton("开始", self.page3)
        self.jilushangpin.setStyleSheet(self.button_style + "QPushButton {border-radius: 10px;}")
        page1_layout3.addWidget(self.jilushangpin)

        select_file_button = QPushButton("选择文件", self)
        select_file_button.setStyleSheet(self.button_style + "QPushButton {border-radius: 10px;}")
        select_file_button.clicked.connect(self.select_file)
        page1_layout4.addWidget(select_file_button)
        self.file_path_input = QLineEdit(self)
        self.file_path_input.setStyleSheet(self.lineedit_style)
        self.file_path_input.setReadOnly(True)
        page1_layout4.addWidget(self.file_path_input)

        # 第四行
        lianjin = QLabel("炼金材料价格记录:", self.page3)
        lianjin.setStyleSheet(self.label_style)
        page1_layout5.addWidget(lianjin)
        self.lianjin_start = QPushButton("开始", self.page3)
        self.lianjin_start.setStyleSheet(self.button_style + "QPushButton {border-radius: 10px;}")
        page1_layout5.addWidget(self.lianjin_start)

        lianjin_select_file_button = QPushButton("选择文件", self)
        lianjin_select_file_button.setStyleSheet(self.button_style + "QPushButton {border-radius: 10px;}")
        lianjin_select_file_button.clicked.connect(self.lianjin_select_file)
        page1_layout6.addWidget(lianjin_select_file_button)
        self.lianjin_file_path_input = QLineEdit(self)
        self.lianjin_file_path_input.setStyleSheet(self.lineedit_style)
        self.lianjin_file_path_input.setReadOnly(True)
        page1_layout6.addWidget(self.lianjin_file_path_input)

        page1_layout0.addLayout(page1_layout1)
        page1_layout0.addWidget(separator)
        page1_layout0.addLayout(page1_layout2)
        page1_layout0.addWidget(separator2)
        page1_layout0.addLayout(page1_layout3)
        page1_layout0.addLayout(page1_layout4)
        page1_layout0.addWidget(separator3)
        page1_layout0.addLayout(page1_layout5)
        page1_layout0.addLayout(page1_layout6)
        page1_layout0.addWidget(separator3)

        page1_layout_total.addLayout(page1_layout0)
        page1_layout0.addStretch()
        page1_layout_total.addStretch()

    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "选择文件", "", "所有文件 (*.*)")
        if file_path:
            self.file_path_input.setText(file_path)

    def lianjin_select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "选择文件", "", "所有文件 (*.*)")
        if file_path:
            self.lianjin_file_path_input.setText(file_path)
    def huqumima(self):
        """获取密码"""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "选择文件", "", "所有文件 (*.*)")
        if file_path:
            self.mima_file_path_input.setText(file_path)
            self.add_items_to_combobox(self.qqnumb)

    def set_banzhuan_log(self, *data):
        """板砖页面的log输出在 log框里"""
        combined_data = " ".join(str(item) for item in data)
        self.edig.insertPlainText(f"{combined_data}\n")

        cursor = self.edig.textCursor()
        # cursor.movePosition(cursor.End)
        self.edig.setTextCursor(cursor)

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
