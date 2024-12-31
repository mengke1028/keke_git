# -*- coding: utf-8 -*-
# Keke.Meng  2024/12/31 8:45
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from QT_5.one import Ui_MainWindow


class MW(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.set_hello)

    def set_hello(self):
        print('hello')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MyWindo = MW()
    MyWindo.show()
    sys.exit(app.exec_())
