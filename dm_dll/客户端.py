import os
import zerorpc
from PIL import Image
import numpy as np


def read_bmp_to_array(file_path):
    try:
        # 打开BMP图片
        image = Image.open(file_path)
        # 将图片转换为NumPy数组
        image_array = np.array(image)
        width, height = image.size
        return image_array, (width, height)
    except Exception as e:
        print(f"读取图片时出现错误: {e}")
        return None


if __name__ == "__main__":
    c = zerorpc.Client()
    # c.connect("tcp://106.54.233.105:8888")
    c.connect("tcp://0.0.0.0:8888")
    image_path = r"C:\Users\Keke.Meng\Desktop\test.bmp"  # 替换为实际要发送的图片路径
    x1, y1, x2, y2 = 552, 126, 663, 194
    color = "ff3132-222222"
    sim = 1.0

    img_dat = read_bmp_to_array(image_path)
    if img_dat is not None:
        img_bytes = img_dat[0].tobytes()
        file_name = os.path.basename(image_path)
        width, height = img_dat[1]

        result = c.perform_ocr(img_bytes, 0, 0, width, height, color, sim, file_name, width, height)
        print(f'OCR 结果: {result}')