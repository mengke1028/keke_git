# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox
import winsound  # Windows系统声音提示
import threading
import time
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import re

# 全局变量：控制查询循环、提示音循环
is_running = False
query_thread = None
is_alerting = False  # 控制提示音循环
alert_thread = None  # 提示音后台线程


# 解析URL中的workDate参数
def get_workdate_from_url(url):
    """从URL中提取workDate参数值，返回YYYY-MM-DD格式字符串"""
    try:
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        if 'workDate' in params and params['workDate']:
            return params['workDate'][0]
        match = re.search(r'workDate=(\d{4}-\d{2}-\d{2})', url)
        if match:
            return match.group(1)
    except:
        pass
    return "2026-01-17"


# 替换URL中的workDate参数
def replace_workdate_in_url(url, new_date):
    """替换URL中的workDate参数为新日期，保持其他参数不变"""
    if not url or not new_date:
        return url
    try:
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        params['workDate'] = [new_date]
        new_query = urlencode(params, doseq=True)
        new_parsed = parsed._replace(query=new_query)
        return urlunparse(new_parsed)
    except:
        pattern = r'workDate=\d{4}-\d{2}-\d{2}'
        if re.search(pattern, url):
            return re.sub(pattern, f'workDate={new_date}', url)
        else:
            sep = '&' if '?' in url else '?'
            return f"{url}{sep}workDate={new_date}"


# 核心查询函数
def get_appointment_status(query_url):
    """查询指定时段的挂号状态"""
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090c37) XWEB/14185 Flue',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/wxpic,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'userId=o6FXZjuLg1FbSrJVM0lRUrDUeIjU; userStr=R9nnF4vuP6LBJX9t6j39ddSMBBB3X6rFXx1lHLE4OHhFlx1tPEbTYsnQBDut%2BFNva8wQvFt%2BmqzB%0D%0AXyF5AJYX%2BLpsko94iBY1YUtKg%2BZwvjaYjxoQXZMF3d%2FrdTkl3%2FR91vwkLEkQgo9FGWt7NyI3eqzf%0D%0A8lBC8XvBBLOHMmyGWo042SrNqS8knlIWDLUKQUoJYndrcvHgP%2Bu91Kxb%2FjqjeRpr%2BaedtTjYQUFb%0D%0AHfizBxnhHx3BUwsj0kLwagfHew6nvce7%2FNVw%2F4ithFwBWGcOtZKuwvsa18VW3%2Ftn5rn1r3P5DIyZ%0D%0ApCzLl2%2FaUb%2BRpiql6hkYQ0rqrJP4f2I06sSC5cewl5Q473qJqid1AxgbCvobLs4V%2BQoQPJl7LRGA%0D%0AIxLkAFSGbHK8Zur94J7tqnJ2dew5%2BSTotV4Gs2bjvbcNCEH0vAU92DRjZTqesxiuwJrzzqq8QSbK%0D%0AeDP8hHUpvvjxvg%3D%3D; needAlert=1; SESSION=3984aa11-cd69-470b-bbe6-f9e16c013c53'
    }
    payload = None
    result = {}
    target_time_slots = [("08:00", "08:30"), ("08:30", "09:00")]

    if not query_url or not query_url.startswith(('http://', 'https://')):
        return {}, "URL无效！请输入以http/https开头的地址"

    try:
        response0 = requests.request(
            "GET", query_url, headers=headers, data=payload, timeout=10
        )
        response0.raise_for_status()
        soup = BeautifulSoup(response0.text, 'html.parser')

        rows = soup.select('.expert_chose table tr')
        for row in rows[1:]:
            start_time_elem = row.find('span', class_='startTime')
            end_time_elem = row.find('span', class_='endTime')
            if not start_time_elem or not end_time_elem:
                continue
            start_time = start_time_elem.text.strip()
            end_time = end_time_elem.text.strip()

            for target_start, target_end in target_time_slots:
                if start_time == target_start and end_time == target_end:
                    reg_btn = row.find('span', class_='reg_yy_btn')
                    tds = row.find_all('td')
                    left_num_elem = tds[2] if len(tds) >= 3 else None
                    left_num = left_num_elem.text.strip() if left_num_elem else '未知'

                    if reg_btn and 'unclick' in reg_btn.get('class', []):
                        status = '已满'
                    else:
                        status = f'有号（余{left_num}）'

                    result[f"{target_start}-{target_end}"] = status

        for ts in target_time_slots:
            key = f"{ts[0]}-{ts[1]}"
            if key not in result:
                result[key] = '未查询到该时段'

        return result, "查询成功"

    except requests.exceptions.RequestException as e:
        return {}, f"网络错误：{str(e)[:50]}..."
    except Exception as e:
        return {}, f"解析错误：{str(e)[:50]}..."


# 后台定时查询循环
def query_loop():
    global is_running
    while is_running:
        selected_date = date_entry.get()
        original_url = url_entry.get().strip()
        current_url = replace_workdate_in_url(original_url, selected_date)
        status_dict, msg = get_appointment_status(current_url)
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")

        root.after(0, update_display, current_time, status_dict, msg, current_url)

        # 检测到有号触发提醒
        has_available = any("有号" in v for v in status_dict.values())
        if has_available:
            root.after(0, show_alert)

        time.sleep(5)


# 更新UI显示区域
def update_display(current_time, status_dict, msg, current_url):
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"🕒 查询时间：{current_time}\n")
    result_text.insert(tk.END,
                       f"🌐 当前URL：{current_url[:80]}...\n" if len(current_url) > 80 else f"🌐 当前URL：{current_url}\n")
    result_text.insert(tk.END, f"📝 状态信息：{msg}\n")
    result_text.insert(tk.END, "=" * 40 + "\n")
    for time_slot, status in status_dict.items():
        if "有号" in status:
            result_text.insert(tk.END, f"⏰ 时段 {time_slot}：", 'red_tag')
            result_text.insert(tk.END, f"{status}\n")
        else:
            result_text.insert(tk.END, f"⏰ 时段 {time_slot}：{status}\n")


# 循环播放提示音（后台线程）
def play_alert_sound():
    """循环播放提示音，直到is_alerting为False"""
    global is_alerting
    while is_alerting:
        winsound.Beep(1000, 900)  # 频率1000Hz，时长800ms
        time.sleep(0.1)  # 间隔0.2秒，避免声音太刺耳
    # 播放停止后恢复按钮状态
    root.after(0, lambda: alert_btn.config(state=tk.DISABLED, text="停止提示音"))


# 有号提醒：循环音+置顶弹窗+按钮激活
def show_alert():
    global is_alerting, alert_thread
    if not is_alerting:
        is_alerting = True
        # 启动提示音后台线程，不阻塞UI
        alert_thread = threading.Thread(target=play_alert_sound, daemon=True)
        alert_thread.start()
        # 激活停止提示音按钮
        alert_btn.config(state=tk.NORMAL, text="停止提示音")
        # 弹出置顶提醒弹窗，点击确定后自动停止提示音
        messagebox.showwarning("🚨 挂号提醒 🚨", "检测到可挂号时段！\n请立即前往页面挂号！\n点击【确定】自动停止提示音")
        # 弹窗关闭后停止提示音
        stop_alert_sound()


# 手动停止提示音
def stop_alert_sound():
    global is_alerting
    is_alerting = False
    alert_btn.config(state=tk.DISABLED, text="提示音未播放")
    stop_query()

# 开始查询
def start_query():
    global is_running, query_thread
    if not is_running:
        is_running = True
        query_thread = threading.Thread(target=query_loop, daemon=True)
        query_thread.start()
        start_btn.config(state=tk.DISABLED)
        stop_btn.config(state=tk.NORMAL)
        result_text.insert(tk.END, "▶️ 已开始定时监控号源（每5秒查询一次）\n")


# 停止查询（同时停止提示音）
def stop_query():
    global is_running
    if is_running:
        is_running = False
        # 停止监控时同步停止提示音
        stop_alert_sound()
        start_btn.config(state=tk.NORMAL)
        stop_btn.config(state=tk.DISABLED)
        result_text.insert(tk.END, "⏹️ 已停止号源监控\n")


# 日期变更时提示
def on_date_change(event=None):
    selected_date = date_entry.get()
    original_url = url_entry.get().strip()
    result_text.insert(tk.END, f"\n🔄 已选择日期：{selected_date}，查询时会自动替换URL中的workDate参数\n")


# 初始化主界面
if __name__ == "__main__":
    root = tk.Tk()
    root.title("苏州妇幼保健院 - 挂号监控工具（循环提示音）")
    root.geometry("650x580")
    root.resizable(True, True)
    # 窗口置顶（可选，取消注释即可）
    # root.attributes('-topmost', True)

    # ========== 1. 标题区域 ==========
    title_label = ttk.Label(
        root,
        text="苏州妇幼保健院 产科（早孕关爱）普通门诊 - 号源监控",
        font=("微软雅黑", 11, "bold")
    )
    title_label.pack(pady=8)

    # ========== 2. 日期选择区域 ==========
    date_frame = ttk.LabelFrame(root, text="挂号日期（单独修改）", padding=(10, 5))
    date_frame.pack(fill=tk.X, padx=15, pady=5)
    default_url = "http://wx.jssz12320.cn/gh/register/normalPool.ha?hospName=%E8%8B%8F%E5%B7%9E%E5%B8%82%E5%A6%87%E5%B9%BC%E4%BF%9D%E5%81%A5%E9%99%A2&departName=%E5%A6%87%E7%A7%91%EF%BC%88%E6%97%A9%E5%AD%95%E5%85%B3%E7%88%B1%EF%BC%89%E6%99%AE%E9%80%9A%E9%97%A8%E8%AF%8A&workDate=2026-01-17&workType=%E4%B8%8A%E5%8D%88"
    default_date = get_workdate_from_url(default_url)

    ttk.Label(date_frame, text="选择日期：", font=("微软雅黑", 9)).grid(row=0, column=0, padx=5, pady=3, sticky=tk.W)
    date_entry = ttk.Entry(date_frame, font=("微软雅黑", 9), width=20)
    date_entry.grid(row=0, column=1, padx=5, pady=3)
    date_entry.insert(0, default_date)
    date_entry.bind('<FocusOut>', on_date_change)
    date_entry.bind('<Return>', on_date_change)
    ttk.Label(date_frame, text="格式：YYYY-MM-DD（例：2026-01-18）", font=("微软雅黑", 8), foreground="gray").grid(row=0, column=2,
                                                                                                        padx=5, pady=3,
                                                                                                        sticky=tk.W)

    # ========== 3. URL输入区域 ==========
    url_frame = ttk.LabelFrame(root, text="查询地址（自动同步日期）", padding=(10, 5))
    url_frame.pack(fill=tk.X, padx=15, pady=5)
    url_entry = ttk.Entry(url_frame, font=("微软雅黑", 9), width=80)
    # url_entry.pack(fill=tk.X, padx=5, pady=3)
    url_entry.insert(0, default_url)

    # ========== 4. 操作按钮区域（新增停止提示音按钮） ==========
    btn_frame = ttk.Frame(root)
    btn_frame.pack(pady=8)
    start_btn = ttk.Button(btn_frame, text="开始监控", command=start_query, width=12)
    start_btn.grid(row=0, column=0, padx=8)
    stop_btn = ttk.Button(btn_frame, text="停止监控", command=stop_query, state=tk.DISABLED, width=12)
    stop_btn.grid(row=0, column=1, padx=8)
    # 新增：停止提示音按钮（默认禁用）
    alert_btn = ttk.Button(btn_frame, text="提示音未播放", command=stop_alert_sound, state=tk.DISABLED, width=12)
    alert_btn.grid(row=0, column=2, padx=8)

    # ========== 5. 结果显示区域 ==========
    result_frame = ttk.LabelFrame(root, text="监控结果", padding=(10, 5))
    result_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
    result_text = tk.Text(result_frame, font=("微软雅黑", 10), wrap=tk.WORD)
    scroll_bar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=result_text.yview)
    result_text.config(yscrollcommand=scroll_bar.set)
    result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
    result_text.tag_config('red_tag', foreground='red', font=("微软雅黑", 10, "bold"))

    # 初始提示
    result_text.insert(tk.END, "💡 核心功能：检测到有号后提示音**循环播放**，支持手动停止\n")
    result_text.insert(tk.END, "💡 单独修改日期，自动同步到URL，无需手动编辑长链接\n")
    result_text.insert(tk.END, "💡 关闭提醒弹窗/点击【停止提示音】/停止监控，均可终止提示音\n")
    result_text.insert(tk.END, "------------------------\n")
    result_text.insert(tk.END, "点击「开始监控」按钮启动号源检测\n")

    # 运行主循环
    root.mainloop()