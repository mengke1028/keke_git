# -*- coding: utf-8 -*-
# TCN01475  2026/1/19 8:40
import tkinter as tk
from tkinter import scrolledtext, messagebox
import random
import time
import json
import os

from libs222.jintu import daili1, xyg
from libs222.软件加登录验证 import login
import win32gui
import ctypes
from libs222.实现移动 import key_press
from libs222.判断SS import find_image_in_region, mk_OCR
from libs222.点击在游戏生效 import click, only_move
from pynput.keyboard import Controller
from datetime import datetime, timedelta
from pynput import keyboard
import threading

# 配置文件路径（相对路径，和脚本同目录）
CONFIG_FILE = "scan_tool_config.json"


class MultiItemScanTool:
    """多物品扫拍工具类 - 封装所有功能（含配置持久化+物品编辑+bug修复+个数统计）"""

    def __init__(self):
        # 1. 主窗口初始化
        self.root = tk.Tk()
        self.root.title("小鱼干扫拍")
        self.root.geometry("+1128+0")  # 660x620+
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f2f5")

        # 2. 全局配置
        self.FONT_NORMAL = ("微软雅黑", 10)
        self.FONT_TITLE = ("微软雅黑", 12, "bold")
        self.FONT_BUTTON = ("微软雅黑", 11, "bold")

        # 3. 核心状态变量（类内属性，替代全局变量）
        self.scan_running = False  # 扫拍运行标志
        self.scan_thread = None  # 扫拍线程对象
        self.item_list = []  # 物品列表: [{"name": str, "price": float, "has_unit": bool}]
        self.editing_index = -1  # 正在编辑的物品索引（-1表示未编辑）

        # 4. 初始化界面
        self._create_ui()

        # 5. 自动加载本地配置
        self._load_config()

        # 6. 修复bug：启动后自动将焦点设置到物品名称输入框，并确保可编辑
        self.new_item_entry.config(state=tk.NORMAL)
        self.new_item_entry.focus_set()

        # 7. 窗口关闭事件绑定（关闭时自动保存配置）
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _create_ui(self):
        """创建所有UI组件（拆分到子方法，结构清晰）"""
        self._create_title_frame()
        self._create_main_frame()
        self._create_btn_frame()
        self._cuoyao_btn_frame()  # 撮药
        self._create_log_frame()

    def _create_title_frame(self):
        """创建标题栏"""
        title_frame = tk.Frame(self.root, bg="#409eff", height=50)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(
            title_frame,
            text="小鱼干扫拍",
            font=self.FONT_TITLE,
            bg="#409eff",
            fg="white",
            anchor="center"
        )
        title_label.pack(expand=True)

    def _create_main_frame(self):
        """创建核心配置区（物品管理+参数）"""
        # 主配置框
        self.main_frame = tk.LabelFrame(
            self.root,
            text="扫拍配置",
            font=self.FONT_TITLE,
            bg="#f0f2f5",
            fg="#303133",
            padx=15,
            pady=10
        )
        self.main_frame.pack(fill=tk.X, padx=20, pady=15)

        # ---------------------- 新增物品输入区 ----------------------
        # 物品名称
        tk.Label(
            self.main_frame,
            text="物品名称：",
            font=self.FONT_NORMAL,
            bg="#f0f2f5",
            fg="#303133"
        ).grid(row=0, column=0, padx=5, pady=8, sticky="e")
        self.new_item_entry = tk.Entry(
            self.main_frame,
            width=15,
            font=self.FONT_NORMAL,
            bd=1,
            relief=tk.SOLID,
            bg="white",
            state=tk.NORMAL  # 显式设置为可编辑
        )
        self.new_item_entry.grid(row=0, column=1, padx=5, pady=8, sticky="w")
        # self.new_item_entry.insert(0, "无色")

        # 目标价格
        tk.Label(
            self.main_frame,
            text="目标价格：",
            font=self.FONT_NORMAL,
            bg="#f0f2f5",
            fg="#303133"
        ).grid(row=0, column=2, padx=5, pady=8, sticky="e")
        self.new_price_entry = tk.Entry(
            self.main_frame,
            width=10,
            font=self.FONT_NORMAL,
            bd=1,
            relief=tk.SOLID,
            bg="white",
            state=tk.NORMAL  # 显式设置为可编辑
        )
        self.new_price_entry.grid(row=0, column=3, padx=5, pady=8, sticky="w")
        # self.new_price_entry.insert(0, "44")

        # 是否有单价（独立选择）
        self.new_has_unit = tk.BooleanVar(value=True)
        unit_check = tk.Checkbutton(
            self.main_frame,
            text="有单价",
            variable=self.new_has_unit,
            font=self.FONT_NORMAL,
            bg="#f0f2f5",
            fg="#303133",
            selectcolor="#f0f2f5",
            bd=0
        )
        unit_check.grid(row=0, column=4, padx=5, pady=8, sticky="w")

        # 添加按钮
        add_btn = tk.Button(
            self.main_frame,
            text="添加物品",
            font=self.FONT_NORMAL,
            bg="#67c23a",
            fg="white",
            bd=0,
            relief=tk.FLAT,
            width=8,
            command=self.add_item
        )
        add_btn.grid(row=0, column=5, padx=5, pady=8)

        # ---------------------- 已选物品列表 ----------------------
        # ★ 修改1：创建带个数的标签（用StringVar实现动态更新）
        self.item_count_var = tk.StringVar(value="已添加物品：0个")
        self.item_count_label = tk.Label(
            self.main_frame,
            textvariable=self.item_count_var,  # 使用变量绑定文本
            font=self.FONT_NORMAL,
            bg="#f0f2f5",
            fg="#303133"
        )
        self.item_count_label.grid(row=1, column=0, padx=5, pady=8, sticky="ne")

        self.item_listbox = tk.Listbox(
            self.main_frame,
            width=55,
            height=4,
            font=self.FONT_NORMAL,
            bd=1,
            relief=tk.SOLID,
            bg="white"
        )
        self.item_listbox.grid(row=1, column=1, columnspan=5, padx=5, pady=8, sticky="w")

        # 操作按钮组（删除+编辑）
        delete_btn = tk.Button(
            self.main_frame,
            text="删除选中",
            font=self.FONT_NORMAL,
            bg="#f56c6c",
            fg="white",
            bd=0,
            relief=tk.FLAT,
            width=8,
            command=self.delete_item
        )
        delete_btn.grid(row=2, column=1, padx=5, pady=8, sticky="w")

        # 编辑选中按钮
        edit_btn = tk.Button(
            self.main_frame,
            text="编辑选中",
            font=self.FONT_NORMAL,
            bg="#ff9f43",
            fg="white",
            bd=0,
            relief=tk.FLAT,
            width=8,
            command=self.edit_item
        )
        edit_btn.grid(row=2, column=2, padx=5, pady=8, sticky="w")

        # ---------------------- 通用参数 ----------------------
        # 随机间隔
        tk.Label(
            self.main_frame,
            text="随机间隔：",
            font=self.FONT_NORMAL,
            bg="#f0f2f5",
            fg="#303133"
        ).grid(row=2, column=3, padx=5, pady=8, sticky="e")
        self.rand_interval = tk.Entry(
            self.main_frame,
            width=10,
            font=self.FONT_NORMAL,
            bd=1,
            relief=tk.SOLID,
            bg="white"
        )
        self.rand_interval.grid(row=2, column=4, padx=5, pady=8, sticky="w")
        self.rand_interval.insert(0, "2-5")

        # 需要初始化（全局）
        self.need_init = tk.BooleanVar(value=True)
        init_check = tk.Checkbutton(
            self.main_frame,
            text="需要初始化",
            variable=self.need_init,
            font=self.FONT_NORMAL,
            bg="#f0f2f5",
            fg="#303133",
            selectcolor="#f0f2f5",
            bd=0
        )
        init_check.grid(row=3, column=4, padx=5, pady=8, sticky="w")

        # ---------------------- 配置保存/加载按钮 ----------------------
        # 保存配置按钮
        save_config_btn = tk.Button(
            self.main_frame,
            text="保存配置",
            font=self.FONT_NORMAL,
            bg="#409eff",
            fg="white",
            bd=0,
            relief=tk.FLAT,
            width=8,
            command=self._save_config
        )
        save_config_btn.grid(row=3, column=1, padx=5, pady=8, sticky="w")

        # 加载配置按钮
        load_config_btn = tk.Button(
            self.main_frame,
            text="加载配置",
            font=self.FONT_NORMAL,
            bg="#909399",
            fg="white",
            bd=0,
            relief=tk.FLAT,
            width=8,
            command=self._load_config
        )
        load_config_btn.grid(row=3, column=2, padx=5, pady=8, sticky="w")

    # ★ 修改2：新增更新物品个数显示的方法
    def update_item_count(self):
        """更新物品个数显示"""
        count = len(self.item_list)
        self.item_count_var.set(f"已添加物品：{count}个")

    def _create_btn_frame(self):
        """创建启动/停止按钮区"""
        btn_frame = tk.Frame(self.root, bg="#f0f2f5")
        btn_frame.pack(fill=tk.X, padx=20, pady=5)

        # 开始按钮
        self.start_btn = tk.Button(
            btn_frame,
            text="开始扫拍",
            font=self.FONT_BUTTON,
            bg="#409eff",
            fg="white",
            bd=0,
            relief=tk.FLAT,
            height=2,
            command=self.start_scan
        )
        self.start_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        # 绑定悬停效果
        self.start_btn.bind("<Enter>", self._on_enter_start)
        self.start_btn.bind("<Leave>", self._on_leave_start)

        # 停止按钮
        self.stop_btn = tk.Button(
            btn_frame,
            text="停止扫拍",
            font=self.FONT_BUTTON,
            bg="#909399",
            fg="white",
            bd=0,
            relief=tk.FLAT,
            height=2,
            command=self.stop_scan,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5, pady=5)
        # 绑定悬停效果
        self.stop_btn.bind("<Enter>", self._on_enter_stop)
        self.stop_btn.bind("<Leave>", self._on_leave_stop)

    def _cuoyao_btn_frame(self):
        btn_frame = tk.Frame(self.root, bg="#f0f2f5")
        btn_frame.pack(fill=tk.X, padx=20, pady=5)
        self.cuoyao_but = tk.Button(
            btn_frame,
            text="开始挫药",
            font=self.FONT_BUTTON,
            bg="#409eff",
            fg="white",
            bd=0,
            relief=tk.FLAT,
            height=2,
            command=self.cuoyao,
            state=tk.NORMAL
        )
        self.cuoyao_but.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5, pady=5)
        # 绑定悬停效果
        self.cuoyao_but.bind("<Enter>", self._on_enter_stop)
        self.cuoyao_but.bind("<Leave>", self._on_leave_stop)

    def _create_log_frame(self):
        """创建日志显示区"""
        log_frame = tk.LabelFrame(
            self.root,
            text="运行日志",
            font=self.FONT_TITLE,
            bg="#f0f2f5",
            fg="#303133",
            padx=10,
            pady=5
        )
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.log = scrolledtext.ScrolledText(
            log_frame,
            font=("Consolas", 10),
            bg="#ffffff",
            fg="#303133",
            bd=1,
            relief=tk.SOLID,
            wrap=tk.WORD
        )
        self.log.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] 群578015844\n", "red")

    # ---------------------- 物品编辑核心功能 ----------------------
    def edit_item(self):
        """编辑选中的物品（弹出编辑窗口）"""
        # 检查是否选中物品
        selected_idx = self.item_listbox.curselection()
        if not selected_idx:
            messagebox.showwarning("提示", "请先选中要编辑的物品！")
            return

        # 获取选中物品的索引和当前配置
        listbox_idx = selected_idx[0]
        self.editing_index = listbox_idx  # 记录正在编辑的索引
        current_item = self.item_list[listbox_idx]

        # 创建编辑窗口
        edit_window = tk.Toplevel(self.root)
        edit_window.title("编辑物品")
        edit_window.geometry("400x220")
        edit_window.resizable(False, False)
        edit_window.configure(bg="#f0f2f5")

        # ---------------------- 编辑窗口组件 ----------------------
        # 物品名称
        tk.Label(
            edit_window,
            text="物品名称：",
            font=self.FONT_NORMAL,
            bg="#f0f2f5",
            fg="#303133"
        ).grid(row=0, column=0, padx=20, pady=20, sticky="e")
        self.edit_item_entry = tk.Entry(
            edit_window,
            width=20,
            font=self.FONT_NORMAL,
            bd=1,
            relief=tk.SOLID,
            bg="white"
        )
        self.edit_item_entry.grid(row=0, column=1, padx=10, pady=20, sticky="w")
        self.edit_item_entry.insert(0, current_item["name"])

        # 目标价格
        tk.Label(
            edit_window,
            text="目标价格：",
            font=self.FONT_NORMAL,
            bg="#f0f2f5",
            fg="#303133"
        ).grid(row=1, column=0, padx=20, pady=10, sticky="e")
        self.edit_price_entry = tk.Entry(
            edit_window,
            width=20,
            font=self.FONT_NORMAL,
            bd=1,
            relief=tk.SOLID,
            bg="white"
        )
        self.edit_price_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.edit_price_entry.insert(0, str(current_item["price"]))

        # 是否有单价
        self.edit_has_unit = tk.BooleanVar(value=current_item["has_unit"])
        unit_check = tk.Checkbutton(
            edit_window,
            text="有单价",
            variable=self.edit_has_unit,
            font=self.FONT_NORMAL,
            bg="#f0f2f5",
            fg="#303133",
            selectcolor="#f0f2f5",
            bd=0
        )
        unit_check.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # 保存编辑按钮
        save_edit_btn = tk.Button(
            edit_window,
            text="保存修改",
            font=self.FONT_NORMAL,
            bg="#409eff",
            fg="white",
            bd=0,
            relief=tk.FLAT,
            width=10,
            command=lambda: self._save_edit(edit_window)
        )
        save_edit_btn.grid(row=3, column=1, padx=10, pady=15, sticky="w")

    def _save_edit(self, edit_window):
        """保存编辑后的物品配置"""
        # 获取编辑后的值
        new_name = self.edit_item_entry.get().strip()
        new_price_str = self.edit_price_entry.get().strip()
        new_has_unit = self.edit_has_unit.get()

        # 非空校验
        if not new_name:
            messagebox.showwarning("提示", "物品名称不能为空！")
            return
        if not new_price_str:
            messagebox.showwarning("提示", "目标价格不能为空！")
            return

        # 价格格式校验
        try:
            new_price = int(new_price_str)
            if new_price <= 0:
                raise ValueError
        except:
            messagebox.showerror("错误", "目标价格请输入正数字！")
            return

        # 重复校验（排除当前编辑的物品）
        for i, item in enumerate(self.item_list):
            if i != self.editing_index and item["name"] == new_name:
                messagebox.showwarning("提示", f"物品「{new_name}」已存在！")
                return

        # 更新物品配置
        old_item = self.item_list[self.editing_index]
        old_info = f"{old_item['name']}（目标价：{old_item['price']} | {'有单价' if old_item['has_unit'] else '无单价'}）"
        new_info = f"{new_name}（目标价：{new_price} | {'有单价' if new_has_unit else '无单价'}）"

        self.item_list[self.editing_index] = {
            "name": new_name,
            "price": new_price,
            "has_unit": new_has_unit
        }

        # 更新UI和日志
        self.update_item_listbox()
        self.update_item_count()  # ★ 修改3：编辑后更新个数
        self._log_msg(f"✏️ 编辑物品：{old_info} → {new_info}")
        messagebox.showinfo("成功", "物品修改成功！")

        # 关闭编辑窗口，重置编辑索引
        edit_window.destroy()
        self.editing_index = -1

    # ---------------------- 配置保存/加载核心方法 ----------------------
    def _save_config(self):
        """保存当前配置到本地JSON文件"""
        try:
            # 组装要保存的配置数据
            config_data = {
                "item_list": self.item_list,
                "rand_interval": self.rand_interval.get().strip(),
                "need_init": self.need_init.get()
            }

            # 写入JSON文件（保证中文正常显示）
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config_data, f, ensure_ascii=False, indent=4)

            self._log_msg("✅ 配置已成功保存到本地（scan_tool_config.json）")
            # 关闭时自动保存不弹窗，手动保存才弹窗
            if self.root.focus_get() is not None:
                messagebox.showinfo("成功", "配置保存成功！")
        except Exception as e:
            self._log_msg(f"❌ 保存配置失败：{str(e)}")
            messagebox.showerror("错误", f"保存配置失败：{str(e)}")

    def _load_config(self):
        """从本地JSON文件加载配置"""
        # 检查配置文件是否存在
        if not os.path.exists(CONFIG_FILE):
            self._log_msg("ℹ️ 未找到本地配置文件，使用默认配置")
            # 加载默认物品（兼容原有逻辑）
            self.add_item()
            # 修复bug：加载默认物品后，确保输入框可编辑
            self.new_item_entry.config(state=tk.NORMAL)
            return

        try:
            # 读取配置文件
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config_data = json.load(f)

            # 加载物品列表
            self.item_list = config_data.get("item_list", [])
            self.update_item_listbox()
            self.update_item_count()  # ★ 修改4：加载配置后更新个数

            # 加载随机间隔
            rand_interval = config_data.get("rand_interval", "2-5")
            self.rand_interval.delete(0, tk.END)
            self.rand_interval.insert(0, rand_interval)

            # 加载需要初始化状态
            need_init = config_data.get("need_init", False)
            self.need_init.set(need_init)

            self._log_msg(f"✅ 成功加载本地配置（共{len(self.item_list)}个物品）")
            # 修复bug：加载配置后，确保输入框可编辑并获取焦点
            self.new_item_entry.config(state=tk.NORMAL)
            self.new_item_entry.focus_set()
        except Exception as e:
            self._log_msg(f"❌ 加载配置失败：{str(e)}")
            messagebox.showerror("错误", f"加载配置失败：{str(e)}")
            # 修复bug：加载失败时，依然确保输入框可编辑
            self.new_item_entry.config(state=tk.NORMAL)

    # ---------------------- 核心业务逻辑 ----------------------
    def add_item(self):
        """添加物品（含参数校验）"""
        # 获取输入值
        item_name = self.new_item_entry.get().strip()
        item_price_str = self.new_price_entry.get().strip()
        has_unit = self.new_has_unit.get()

        # 非空校验
        if not item_name:
            self._log_msg("⚠️ 物品名称不能为空！")
            return
        if not item_price_str:
            self._log_msg("⚠️ 目标价格不能为空！")
            return

        # 价格格式校验
        try:
            item_price = int(item_price_str)
            if item_price <= 0:
                raise ValueError
        except:
            self._log_msg("⚠️ 目标价格请输入正数字！")
            return

        # 重复校验
        for item in self.item_list:
            if item["name"] == item_name:
                self._log_msg(f"⚠️ 物品「{item_name}」已存在！")
                return

        # 添加到列表并更新UI
        self.item_list.append({
            "name": item_name,
            "price": item_price,
            "has_unit": has_unit
        })
        self.update_item_listbox()
        self.update_item_count()  # ★ 修改5：添加物品后更新个数
        # 清空输入框，并确保输入框依然可编辑
        self.new_item_entry.delete(0, tk.END)
        self.new_price_entry.delete(0, tk.END)
        self.new_item_entry.config(state=tk.NORMAL)  # 显式保持可编辑
        self.new_item_entry.focus_set()  # 清空后自动获取焦点，方便连续添加
        # 日志反馈
        unit_text = "有单价" if has_unit else "无单价"
        self._log_msg(f"添加物品：{item_name}（目标价：{item_price} | {unit_text}）")

    def delete_item(self):
        """删除选中的物品"""
        selected_idx = self.item_listbox.curselection()
        if not selected_idx:
            messagebox.showwarning("提示", "请先选中要删除的物品！")
            return

        # 获取选中项信息并删除
        selected_text = self.item_listbox.get(selected_idx)
        item_name = selected_text.split(" | ")[0].split(" - ")[0]
        for i, item in enumerate(self.item_list):
            if item["name"] == item_name:
                del self.item_list[i]
                break

        # 更新UI和日志
        self.update_item_listbox()
        self.update_item_count()  # ★ 修改6：删除物品后更新个数
        self._log_msg(f"🗑️ 删除物品：{selected_text}")

    def start_scan(self):
        """启动多物品扫拍"""
        # 空列表校验
        # print(self.item_list)
        if not self.item_list:
            self._log_msg("⚠️ 请先添加至少一个物品！")
            return

        # 间隔参数校验
        interval_str = self.rand_interval.get().strip()
        if "-" not in interval_str:
            self._log_msg("⚠️ 随机间隔请填「2-5」格式！")
            return
        try:
            min_t, max_t = map(int, interval_str.split("-"))
            if min_t > max_t or min_t < 1:
                raise ValueError
        except:
            self._log_msg("⚠️ 随机间隔请填有效范围（如1-10）！")
            return

        # 更新状态和按钮
        self.scan_running = True
        self.start_btn.config(state=tk.DISABLED, bg="#909399")
        self.stop_btn.config(state=tk.NORMAL, bg="#f56c6c")

        # 日志反馈
        init_text = "需要初始化" if self.need_init.get() else "无需初始化"
        self._log_msg(f"开始多物品扫拍（共{len(self.item_list)}个 | {init_text}）")

        # 启动扫拍线程
        try:
            INIT_all()
            # self.scan_thread = Thread(target=self._scan_task, args=(min_t, max_t), daemon=True)
            # self.scan_thread.start()
            self.thread = threading.Thread(target=self._scan_task)
            self.thread.daemon = True
            self.thread.start()

        except Exception as e:
            self._log_msg('没有游戏窗口, 确认工具是否用了管理员权限打开')
            self.scan_running = False
            self.start_btn.config(state=tk.NORMAL, bg="#409eff")
            self.stop_btn.config(state=tk.DISABLED, bg="#909399")

    def stop_scan(self):
        """停止扫拍"""


        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(self.thread.ident), ctypes.py_object(SystemExit))
        # 恢复按钮状态
        self.start_btn.config(state=tk.NORMAL, bg="#409eff")
        self.stop_btn.config(state=tk.DISABLED, bg="#909399")
        self._log_msg("✅ 扫拍任务已停止")

    def cuoyao(self):
        """撮药"""
        print(time.time())
        # global running
        # if running:
        #     pass

    def kaishicuoyao(self):
        """开始挫药"""
        print(12)
        # while True:
        #     click(100, 100)
        #     time.sleep(2)

    def _scan_task(self):
        """扫拍核心任务（内部方法）"""
        INIT_all()
        if 1 == self.need_init.get():  # 是否初始化
            time.sleep(1)
            int_paimai()
        try:
            flags = True
            while self.scan_running:
                # 遍历所有物品扫拍
                for item in self.item_list:
                    if not self.scan_running:
                        break

                    # ------------------24点关闭弹窗------------------------------------
                    if get_time_now():  # 凌晨23:55分会停止测试 等待10分钟后再开始
                        guanbi = find_pic(path + "\\img\\关闭.bmp")
                        if guanbi != -1:
                            print("找到关闭")
                            time.sleep(1)
                            click(guanbi[1], guanbi[2])
                            time.sleep(1)
                    # ------------------24点关闭弹窗------------------------------------

                    # 模拟获取价格
                    name = item['name']  # 名称
                    goumai = int(item['price'])  # 购买价格
                    youdanjia = int(item['has_unit'])  # 是否有单价

                    # ------------------随机间隔------------------------------------
                    suijijiange = self.rand_interval.get()
                    if "-" in suijijiange:
                        datasss = suijijiange.split("-")
                        entry = generate_random_number(int(datasss[0]), int(datasss[-1]))  # # 获得随机间隔时间
                    else:
                        entry = float(suijijiange)

                    time.sleep(entry)
                    if not self.scan_running:
                        break
                    # ------------------随机间隔------------------------------------

                    # ------------------判断是否需要初始化 输入名字------------------------------------
                    find_name(name, len(self.item_list), flags)
                    flags = False
                    # ------------------判断是否需要初始化------------------------------------

                    # ------------------扫拍主体------------------------------------
                    # click(658, 89)
                    only_move(632, 141)
                    if youdanjia == 1:
                        jiage = self.OCR(name)
                        print(jiage)
                    else:
                        jiage = self.OCR2(name)
                    if jiage is None:
                        int_paimai()
                        continue
                    elif jiage <= goumai:
                        self._log_msg("符合要求开始购买\n")
                        click(623, 137)
                        time.sleep(0.1)
                        click(623, 140)
                        time.sleep(0.1)
                        key_press("ENTER")
                        click(623, 140)
                        key_press("ENTER")
                        key_press("ENTER")
                        key_press("ENTER")
                        key_press("ENTER")
                        time.sleep(0.5)
                        key_press("SPACE")
                if not self.scan_running:
                    break
                # 随机间隔等待

        except Exception as e:
            self._log_msg(f"❌ 扫拍出错：{str(e)}")

    # ---------------------- 辅助方法 ----------------------
    def update_item_listbox(self):
        """更新物品列表框显示"""
        self.item_listbox.delete(0, tk.END)
        for item in self.item_list:
            unit_text = "有单价" if item["has_unit"] else "无单价"
            display_text = f"{item['name']} - 目标价：{item['price']} | {unit_text}"
            self.item_listbox.insert(tk.END, display_text)

    def _log_msg(self, msg):
        """统一日志输出方法"""
        print(msg)
        time_str = time.strftime("%H:%M:%S")
        self.log.insert(tk.END, f"[{time_str}] {msg}\n")
        self.log.see(tk.END)  # 自动滚动到最新日志

    def _on_enter_start(self, e):
        """开始按钮悬停效果"""
        if self.start_btn["state"] == tk.NORMAL:
            self.start_btn.config(bg="#337ecc", fg="white")

    def _on_leave_start(self, e):
        """开始按钮离开效果"""
        if self.start_btn["state"] == tk.NORMAL:
            self.start_btn.config(bg="#409eff", fg="white")

    def _on_enter_stop(self, e):
        """停止按钮悬停效果"""
        if self.stop_btn["state"] == tk.NORMAL:
            self.stop_btn.config(bg="#e64340", fg="white")

    def _on_leave_stop(self, e):
        """停止按钮离开效果"""
        if self.stop_btn["state"] == tk.NORMAL:
            self.stop_btn.config(bg="#f56c6c", fg="white")

    def _on_closing(self):
        """窗口关闭时的安全退出（自动保存配置）"""
        # 关闭前自动保存配置（不弹窗）
        try:
            config_data = {
                "item_list": self.item_list,
                "rand_interval": self.rand_interval.get().strip(),
                "need_init": self.need_init.get()
            }
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config_data, f, ensure_ascii=False, indent=4)
            self._log_msg("✅ 关闭时自动保存配置成功")
        except Exception as e:
            self._log_msg(f"❌ 关闭时保存配置失败：{str(e)}")
        # 停止扫拍线程
        self.scan_running = False
        if self.scan_thread and self.scan_thread.is_alive():
            self.scan_thread.join(timeout=1)
        self.root.destroy()

    def run(self):
        """启动工具主循环"""
        self.root.mainloop()

    def OCR(self, name):
        timout = time.time() + 5
        while True:
            time.sleep(0.5)
            if timout < time.time():
                return
            try:
                res = mk_OCR(492, 136, 661, 155, [254, 255], 0.99)
                print('res', res)
                data = "".join(list(filter(str.isdigit, res)))
                if data != "":
                    # current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self._log_msg(f"{name}: {data}")
                return int(data)
            except:
                continue

    def OCR2(self, name):
        timout = time.time() + 5
        while True:
            time.sleep(0.5)
            if timout < time.time():
                return
            try:
                res = mk_OCR(520, 127, 624, 145, [179, 181, 180, 182, 183], 0.99)
                data = "".join(list(filter(str.isdigit, res)))
                if data != "":
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # self.log.insert("1.0", f"{current_time}-{name}: {data}\n")
                    self._log_msg(f"{name}: {data}")
                return int(data)
            except:
                continue



def INIT_all():
    """初始化窗口"""
    print('移动窗口')
    DNF_CK = win32gui.FindWindow("地下城与勇士", "地下城与勇士：创新世纪")
    win32gui.SetForegroundWindow(DNF_CK)
    xpos = 0
    ypos = 0
    width = 800
    length = 600
    win32gui.MoveWindow(DNF_CK, xpos, ypos, width, length, True)


def int_paimai():
    """打开拍卖行 并初始化"""
    global moren
    # key_press("ESC")
    # time.sleep(0.1)
    while True:
        key_press("B")
        time.sleep(0.1)
        print(path + "\\img\\默认.bmp")
        resp = find_pic(path + "\\img\\默认.bmp")
        if resp:
            print("拍卖行打开")
            moren = resp
            click(moren[0], moren[1])
            click(moren[0], moren[1])
            return
        key_press("ESC")
        time.sleep(0.5)


def int_moren():
    """打开拍卖行 并初始化"""
    global moren
    if moren:
        print("点击默认")
        click(moren[0], moren[1])
        return


def find_pic(img, xpos=0, ypos=0, width=800, length=600):
    """在当前页面找指定图片"""
    resp_mxt = find_image_in_region(xpos, ypos, width, length, img, 0.95, 5)
    if "-1" not in str(resp_mxt):
        X = resp_mxt[-2]
        Y = resp_mxt[-1]
        print("找到图")
        return int(X), int(Y)
    else:
        return -1


def find_name(name, numb, flag):
    """输入要扫的材料名"""
    if numb > 1:
        morenX = moren[0]
        morenY = moren[1]
        click(morenX, morenY)
        time.sleep(0.5)
        click(morenX, morenY)
        flag = True
    if flag:
        click(55, 89)
        keyboard = Controller()
        keyboard.type(name)
        time.sleep(0.5)
    click(658, 89)


def get_time_now(grace_minutes=5):
    """获取当前时间 小时"""
    now = datetime.now()
    current_minute = now.minute
    current_hour = now.hour
    if current_minute >= 60 - grace_minutes:
        next_hour = (current_hour + 1) % 24
        target_time = now.replace(hour=next_hour, minute=0, second=0, microsecond=0)
        if next_hour < current_hour:
            target_time += timedelta(days=1)
            time.sleep(600)
            return True


def generate_random_number(min_val=1.0, max_val=3.0, precision=1):
    """
    生成指定区间内的随机小数，精确到指定小数位数
    参数:
    - min_val: 最小值 (包含)
    - max_val: 最大值 (包含)
    - precision: 小数位数
    """
    random_num = random.uniform(min_val, max_val)
    rounded_num = round(random_num, precision)
    if rounded_num < min_val:
        rounded_num = min_val
    else:
        if rounded_num > max_val:
            rounded_num = max_val
    return rounded_num


# ---------------------- 程序入口 ----------------------
if __name__ == "__main__":
    # 创建工具实例并运行
    running = False
    # thread = None
    # running2 = True
    # thread2 = None
    path = os.path.abspath(".")
    print(path)
    operation = None

    if xyg() == False and daili1() == False:
        res = ctypes.windll.user32.MessageBoxW(0, "此电脑可能未登记，点击确定开始试用", "标题", 1)
        if res == 1:
            print('点击确定')
            # app = MultiPageApp()
            # app.mainloop()
            login = login()
            if not login.run():
                exit()
            else:
                scan_tool = MultiItemScanTool()
                scan_tool.run()
                # saopaiapp.bind_all("<Home>", saopaiapp.start_pause)
                # with keyboard.Listener(on_press=saopaiapp.on_press) as listener:
                #     saopaiapp.mainloop()
        else:
            print('点击取消')
            exit()
    else:
        scan_tool = MultiItemScanTool()
        a = scan_tool.root
        a.bind_all("<Home>", scan_tool.cuoyao)
        with keyboard.Listener(on_press=scan_tool.kaishicuoyao) as listener:
            scan_tool.root.mainloop()
        scan_tool.run()
