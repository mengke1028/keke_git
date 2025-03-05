import tkinter as tk
from tkinter import filedialog


def get_set_pwd(file_path):
    if file_path:
        try:
            # 读取文件所有行
            with open(file_path, 'r', encoding='utf-8') as fp:
                lines = fp.readlines()

            if lines:
                # 读取第一行
                first_line = lines.pop(0).strip()
                print(f"文件第一行内容为: {first_line}")

                # 要新增的行内容，这里示例为 'New line added'，你可以根据需求修改
                new_line = '\n'+first_line
                lines.append(new_line)

                # 将修改后的内容写回文件
                with open(file_path, 'w', encoding='utf-8') as fp:
                    fp.writelines(lines)

                print("第一行已删除，新行已添加。")
                return first_line
            else:
                print("文件为空，没有可删除的行。")
        except FileNotFoundError:
            print("文件未找到，请检查文件路径。")
        except Exception as e:
            print(f"处理文件时出现错误: {e}")
    else:
        print("请先选择文件")

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, file_path)


def start_process():
    # 获取密码
    file_path = path_entry.get()
    first_line = get_set_pwd(file_path)
    if first_line:
        result = first_line.split(',')
        qq = result[0]
        pwd = result[1]



# 创建主窗口
root = tk.Tk()
root.title("文件选择与处理")

# 创建输入框用于显示文件路径
path_entry = tk.Entry(root, width=30)
path_entry.grid(row=0, column=0, padx=5, pady=5)

# 创建选择文件按钮
select_button = tk.Button(root, text="选择文件", command=select_file)
select_button.grid(row=0, column=1, padx=5, pady=5)

# 创建开始按钮，占用两行两列
start_button = tk.Button(root, text="开始", command=start_process)
start_button.grid(row=0, column=2, rowspan=2, columnspan=2, padx=5, pady=5, sticky="nsew")

# 配置列和行的权重，使按钮能根据窗口大小自适应
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# 运行主循环
root.mainloop()