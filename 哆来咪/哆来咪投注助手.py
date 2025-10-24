# -*- coding: utf-8 -*-
import requests
from datetime import datetime, timedelta
import time
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import configparser
import os

# 配置文件路径
CONFIG_FILE = "bet_config.ini"


class LotteryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("哆来咪投注助手")
        self.root.geometry("700x600")
        self.root.resizable(True, True)

        # 控制程序运行状态 & 新增连续投注次数记录
        self.running = False
        self.xiazhuer = 0
        self.fanbeicishu = 0
        self.headers = {}
        self.continuous_bet_count = 0  # 连续投注次数计数器

        # 先创建UI组件（确保log_text先初始化）
        self.create_widgets()

        # 再加载本地配置（此时log()方法可用）
        self.load_config()

    def create_widgets(self):
        # 输入区域
        input_frame = tk.LabelFrame(self.root, text="配置参数", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Authorization
        tk.Label(input_frame, text="Authorization:").grid(row=0, column=0, sticky="w", pady=5)
        self.auth_entry = tk.Entry(input_frame, width=50)
        self.auth_entry.grid(row=0, column=1, pady=5, columnspan=2)

        # 投注数
        tk.Label(input_frame, text="投注数:").grid(row=1, column=0, sticky="w", pady=5)
        self.xiazhu_entry = tk.Entry(input_frame, width=20)
        self.xiazhu_entry.grid(row=1, column=1, sticky="w", pady=5)

        # 最大翻倍次数
        tk.Label(input_frame, text="最大翻倍次数:").grid(row=2, column=0, sticky="w", pady=5)
        self.fanbei_entry = tk.Entry(input_frame, width=20)
        self.fanbei_entry.grid(row=2, column=1, sticky="w", pady=5)

        # 按钮区域（调整为右对齐）
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=5, anchor="e")  # anchor="e" 实现右对齐

        # 按钮调整为右对齐排列
        self.stop_btn = tk.Button(btn_frame, text="停止运行", command=self.stop_run, state="disabled")
        self.stop_btn.pack(side="right", padx=5)

        self.start_btn = tk.Button(btn_frame, text="开始运行", command=self.start_run)
        self.start_btn.pack(side="right", padx=5)

        # 新增连续投注次数显示标签
        self.bet_count_label = tk.Label(btn_frame, text="当前连续投注次数：0")
        self.bet_count_label.pack(side="left", padx=10)


        # 日志区域
        log_frame = tk.LabelFrame(self.root, text="运行日志", padx=10, pady=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD)
        self.log_text.pack(fill="both", expand=True)
        self.log_text.config(state="disabled")

    def log(self, message):
        """添加日志到文本区域"""
        self.log_text.config(state="normal")
        time_str = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{time_str}] {message}\n")
        self.log_text.see(tk.END)  # 滚动到最新内容
        self.log_text.config(state="disabled")

    def update_bet_count_display(self):
        """更新连续投注次数显示"""
        self.bet_count_label.config(text=f"当前连续投注次数：{self.continuous_bet_count}")

    def reset_bet_count(self):
        """重置连续投注次数（如程序停止、盈利成功时）"""
        self.update_bet_count_display()
        self.log("连续投注次数已重置")

    def increment_bet_count(self):
        """增加连续投注次数"""
        self.continuous_bet_count += 1
        print(self.continuous_bet_count)
        self.update_bet_count_display()
        self.log(f"连续投注次数更新为：{self.continuous_bet_count}")

    def load_config(self):
        """从本地配置文件加载数据"""
        if not os.path.exists(CONFIG_FILE):
            self.log("未找到配置文件，将使用默认设置")
            return

        try:
            config = configparser.ConfigParser()
            config.read(CONFIG_FILE, encoding="utf-8")

            # 读取配置项
            self.saved_auth = config.get("Settings", "authorization", fallback="")
            self.saved_xiazhu = config.get("Settings", "xiazhuer", fallback="")
            self.saved_fanbei = config.get("Settings", "fanbeicishu", fallback="")

            # 填充到输入框
            self.auth_entry.insert(0, self.saved_auth)
            self.xiazhu_entry.insert(0, self.saved_xiazhu)
            self.fanbei_entry.insert(0, self.saved_fanbei)

            self.log("配置文件加载成功")
        except Exception as e:
            self.log(f"加载配置文件失败：{e}")

    def save_config(self):
        """保存当前输入的信息到本地配置文件"""
        try:
            config = configparser.ConfigParser()
            config["Settings"] = {
                "authorization": self.auth_entry.get().strip(),
                "xiazhuer": self.xiazhu_entry.get().strip(),
                "fanbeicishu": self.fanbei_entry.get().strip(),
                "last_save_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                config.write(f)

            self.log("配置信息已保存到本地")
        except Exception as e:
            self.log(f"保存配置文件失败：{e}")

    def get_http_server_time(self, url='https://www.baidu.com'):
        """从 HTTP 响应头获取服务器时间，转换为北京时间"""
        try:
            response = requests.head(url, timeout=5)
            date_str = response.headers.get('Date')
            if not date_str:
                return None
            utc_time = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S GMT")
            beijing_time = utc_time + timedelta(hours=8)
            server_time = str(beijing_time)
            server_time2 = server_time[-2:]
            return server_time2
        except Exception as e:
            self.log(f"获取 HTTP 时间失败：{e}")
            return None

    def get_data(self):
        try:
            url = 'https://api.lzd668.com/api/game/home/3'
            res = requests.get(url, headers=self.headers)
            data = res.json()
            all_list = data['list']
            draw_time = self.get_http_server_time()

            periodId = all_list[3]["id"]
            draw_no_arr1 = all_list[4]["draw_no_arr"][0]
            draw_no_arr2 = all_list[5]["draw_no_arr"][0]
            numb = (str(draw_no_arr1 + draw_no_arr2))[-1]

            draw_money = all_list[4]['draw_money']
            win_money = all_list[4]['win_money']

            if draw_money != '0' and win_money == '0':
                yingli = False
                self.log('盈利失败')
            else:
                yingli = True
                self.log('盈利成功')
                self.reset_bet_count()  # 盈利成功时重置连续投注次数

            datas = {
                'draw_time': draw_time,
                'periodId': periodId,
                'numb': numb,
                'yingli': yingli
            }
            return datas
        except Exception as e:
            self.log(f"获取数据失败：{e}")
            return None

    def xiazhu(self, numb, periodId, xiazhuer=5193):
        try:
            url = 'https://api.lzd668.com/api/game/gameJoin/3'

            dange_xiahuer = str(int(xiazhuer / 9))
            bet_num = [dange_xiahuer for _ in range(10)]

            if numb != '0':
                bet_num[int(numb) - 1] = '0'
            else:
                bet_num[9] = '0'

            json_data = {
                "bet_num": bet_num,
                "total": xiazhuer,
                "periodId": periodId
            }
            response = requests.post(url, headers=self.headers, json=json_data)
            self.increment_bet_count()  # 投注成功时增加连续投注次数
            self.log(json_data)
            self.log(f"投注请求已发送，periodId: {periodId}，投注金额: {xiazhuer}")
            return response
        except Exception as e:
            self.log(f"投注失败：{e}")
            return None

    def run_loop(self):
        """运行循环逻辑"""
        shibaicushu = 0
        current_xiazhuer = self.xiazhuer

        while self.running:
            datas = self.get_data()
            if not datas:
                time.sleep(5)
                continue

            try:
                stop_time_numb = int(datas['draw_time'])
                self.log(f"当前时间数值：{stop_time_numb}")

                if 50 > stop_time_numb > 20:
                    self.log('可以下注')
                    if datas['yingli']:
                        shibaicushu = 0
                        current_xiazhuer = self.xiazhuer  # 重置为初始投注数
                    else:
                        shibaicushu += 1
                        if shibaicushu < self.fanbeicishu:
                            current_xiazhuer = 12 * current_xiazhuer
                            self.log(f"连续失败{shibaicushu}次，翻倍投注为：{current_xiazhuer}")

                    periodId = datas['periodId']
                    numb = datas['numb']
                    self.xiazhu(numb, periodId, current_xiazhuer)
                    time.sleep(40)
                else:
                    self.log(f"{stop_time_numb}，等待5秒再下注")
                    time.sleep(5)
            except Exception as e:
                self.log(f"循环执行错误：{e}")
                time.sleep(5)

        self.reset_bet_count()  # 程序停止时重置连续投注次数
        self.log("程序已停止运行")

    def start_run(self):
        """开始运行"""
        # 获取输入参数
        auth = self.auth_entry.get().strip()
        xiazhu_str = self.xiazhu_entry.get().strip()
        fanbei_str = self.fanbei_entry.get().strip()

        # 验证输入
        if not auth:
            messagebox.showerror("错误", "请输入Authorization")
            return
        if not xiazhu_str or not xiazhu_str.isdigit():
            messagebox.showerror("错误", "请输入有效的投注数")
            return
        if not fanbei_str or not fanbei_str.isdigit():
            messagebox.showerror("错误", "请输入有效的最大翻倍次数")
            return

        # 保存配置到本地
        self.save_config()

        # 保存参数 & 重置连续投注次数
        self.headers = {'Authorization': auth}
        self.xiazhuer = int(xiazhu_str)
        self.fanbeicishu = int(fanbei_str)
        self.running = True
        self.reset_bet_count()

        # 更新按钮状态
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.log("程序开始运行...")

        # 在新线程中运行主逻辑，避免界面卡顿
        threading.Thread(target=self.run_loop, daemon=True).start()

    def stop_run(self):
        """停止运行"""
        self.running = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.log("正在停止程序...")


if __name__ == '__main__':
    root = tk.Tk()
    app = LotteryApp(root)
    root.mainloop()