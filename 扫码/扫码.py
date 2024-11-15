import pyzbar.pyzbar as pyzbar
from PIL import Image

# 读取包含二维码或条形码的图片
img = Image.open('qrcode_with_logo.png')

# 解码图片中的二维码或条形码
decoded_objects = pyzbar.decode(img)

for obj in decoded_objects:
    print(f"Type: {obj.type}")
    print(f"Data: {obj.data.decode('utf-8')}")

