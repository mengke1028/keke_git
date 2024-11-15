import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 使窗口始终置顶
        # 设置窗口标题
        self.setWindowTitle("PyQt5 输入框示例")

        # 布局管理器
        layout = QVBoxLayout()

        # 创建一个输入框
        self.lineEdit = QLineEdit(self)
        layout.addWidget(self.lineEdit)

        # 创建一个按钮
        self.button = QPushButton("获取文本", self)
        layout.addWidget(self.button)

        # 当按钮被点击时触发的动作
        self.button.clicked.connect(self.on_click)

        # 显示标签用于输出结果
        self.label = QLabel("", self)
        layout.addWidget(self.label)

        # 设置布局
        self.setLayout(layout)

    def on_click(self):
        # 获取输入框中的文本
        text = self.lineEdit.text()
        # 更新标签内容
        self.label.setText(f"您输入的是: {text}")


# 主函数
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec_())
