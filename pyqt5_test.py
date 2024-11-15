import sys
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt  # 导入Qt模块以使用AlignCenter

app = QApplication(sys.argv)
label = QLabel('Hello PyQt5!', alignment=Qt.AlignCenter)  # 使用Qt.AlignCenter
label.show()
sys.exit(app.exec_())
