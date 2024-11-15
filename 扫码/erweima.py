import qrcode
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox


def show_image(image):
    # 创建一个新的tkinter窗口
    image_window = tk.Toplevel(root)
    image_window.title("生成的二维码")

    # 将PIL图像转换为tkinter兼容的格式
    photo = ImageTk.PhotoImage(image)

    # 创建一个标签来显示图像
    label = tk.Label(image_window, image=photo)
    label.image = photo  # 防止图像被垃圾回收
    label.pack()


def generate_qr_code():
    # 获取输入框中的数据
    data = entry.get()
    if not data:
        messagebox.showerror("错误", "请输入二维码的内容")
        return

    # 创建QRCode对象
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # 使用高错误纠正能力
        box_size=10,
        border=4,
    )

    # 添加数据到QRCode对象
    qr.add_data("hello".encode('GBK'))
    qr.make(fit=True)

    # 创建二维码图像
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # 如果选择了Logo图片
    if logo_path.get():
        try:
            # 打开要嵌入的图像
            logo = Image.open(logo_path.get())

            # 计算二维码的大小和Logo的位置
            qr_width, qr_height = img.size
            logo_width, logo_height = logo.size

            # 确保Logo大小不超过二维码的1/4
            max_logo_size = min(qr_width, qr_height) // 4
            if logo_width > max_logo_size or logo_height > max_logo_size:
                logo = logo.resize((max_logo_size, max_logo_size), Image.ANTIALIAS)
                logo_width, logo_height = logo.size

            # 计算Logo的位置
            logo_position = ((qr_width - logo_width) // 2, (qr_height - logo_height) // 2)

            # 将Logo粘贴到二维码图像的中心
            img.paste(logo, logo_position)
        except Exception as e:
            messagebox.showerror("错误", f"无法打开Logo图片: {e}")
            return

    # 保存带有Logo的二维码图像
    img.save("二维码.png")
    # messagebox.showinfo("成功", "带有Logo的二维码已生成并保存为 qrcode_with_logo.png")
    show_image(img)

def select_logo_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        logo_path.set(file_path)
        logo_label.config(text=f"选择的Logo: {file_path}")


# 创建主窗口
root = tk.Tk()
root.title("二维码生成器")

# 输入框
entry_label = tk.Label(root, text="输入二维码的内容:")
entry_label.pack(pady=10)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

# 选择Logo图片
logo_path = tk.StringVar()
logo_button = tk.Button(root, text="选择Logo图片", command=select_logo_file)
logo_button.pack(pady=5)
logo_label = tk.Label(root, text="未选择Logo")
logo_label.pack(pady=5)

# 生成按钮
generate_button = tk.Button(root, text="生成二维码", command=generate_qr_code)
generate_button.pack(pady=20)

# 运行主循环
root.mainloop()
