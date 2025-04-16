import ctypes
import os
import zerorpc
import numpy as np
from PIL import Image
import win32com.client

# 加载相关 DLL 文件
patch = ctypes.windll.LoadLibrary(r'D:\keke\dm_dll\momoreg.dll')
patch.SetDllPathW(r'D:\keke\dm_dll\momo.dll', 0)

# 初始化大漠插件
dm = win32com.client.Dispatch('dm.dmsoft')
dm.setDict(0,  r'D:\keke\dm_dll\MK字库_1.txt')
dm.useDict(0)
dmversion = dm.Ver()


class OCRService(object):
    def perform_ocr(self, img_bytes, x1, y1, x2, y2, color, sim, file_name, width, height):
        try:
            # 将字节流数据转换回 numpy.ndarray
            img_dat = np.frombuffer(img_bytes, dtype=np.uint8)

            # 根据图片尺寸调整形状，假设为 RGB 格式
            img_shape = (height, width, 3)
            img_dat = img_dat.reshape(img_shape)

            # 将 numpy.ndarray 保存为图片文件
            img = Image.fromarray(img_dat)
            img.save(file_name)

            print(f"文件 {file_name} 接收成功")

            # 调用大漠插件进行文字识别
            print(x1, y1, x2, y2, file_name, color, sim)
            result = dm.OcrInFile(x1, y1, x2, y2, file_name, color, sim)
            return result
        except Exception as e:
            print(f"处理请求时出错: {e}")
            return str(e)


if __name__ == "__main__":
    s = zerorpc.Server(OCRService())
    s.bind("tcp://0.0.0.0:8888")
    print("服务端已启动，监听端口 4242...")
    s.run()