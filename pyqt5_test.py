# import sys
# from PyQt5.QtWidgets import QApplication, QLabel
# from PyQt5.QtCore import Qt  # 导入Qt模块以使用AlignCenter
#
# app = QApplication(sys.argv)
# label = QLabel('Hello PyQt5!', alignment=Qt.AlignCenter)  # 使用Qt.AlignCenter
# label.show()
# sys.exit(app.exec_())
import random

a = 5.0
b = 10.0
random_float = random.uniform(a, b)
formatted_float_0_to_1 = f"{random_float:.3f}"
print(type(formatted_float_0_to_1))
print(f"Random float between {a} and {b}: {formatted_float_0_to_1}")

