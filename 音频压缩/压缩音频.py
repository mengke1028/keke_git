import soundfile as sf
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import glob

# 定义压缩标志（可自行修改，比如改为 _small 或 _compressed_16k）
COMPRESS_FLAG = "_compressed"


def compress_audio_smaller(input_file, output_file,
                           mono=True,  # 转单声道 ✓
                           sample_rate=16000,  # 降低采样率 ✓
                           subtype='PCM_16',  # 16位或8位
                           block_size=1024 * 100):  # 分块大小（可调整）
    """
    压缩音频文件 - 分块处理超大文件，避免内存不足
    不依赖 ffmpeg/opus
    """
    try:
        # 先获取原始音频信息（不加载全部数据）
        with sf.SoundFile(input_file) as f:
            orig_sr = f.samplerate
            orig_channels = f.channels
            orig_frames = f.frames
            orig_size = os.path.getsize(input_file) / 1024 / 1024

        print(f"处理文件: {os.path.basename(input_file)}")
        print(f"原始信息: 采样率={orig_sr}, 声道={orig_channels}, 总帧数={orig_frames}")

        # 计算采样率转换比例
        ratio = orig_sr / sample_rate if sample_rate < orig_sr else 1.0
        ratio_int = int(np.round(ratio))  # 取整用于下采样

        # 分块读取并写入
        with sf.SoundFile(input_file, 'r') as infile, \
                sf.SoundFile(output_file, 'w', samplerate=sample_rate,
                             channels=1 if (mono and orig_channels > 1) else orig_channels,
                             subtype=subtype) as outfile:

            # 逐块处理
            total_blocks = orig_frames // block_size + 1
            processed_blocks = 0

            while True:
                # 读取一块数据
                block = infile.read(block_size, dtype='float64')
                if len(block) == 0:
                    break  # 读取完毕

                processed_blocks += 1
                if processed_blocks % 10 == 0:  # 每10块打印一次进度
                    print(f"  进度: {processed_blocks}/{total_blocks} 块")

                # 1. 转单声道
                if mono and orig_channels > 1:
                    block = block.mean(axis=1)  # 双声道转单声道

                # 2. 降低采样率（下采样）
                if sample_rate < orig_sr:
                    # 每隔ratio_int个点取一个，保证采样率降低到目标值
                    block = block[::ratio_int]

                # 3. 写入当前块
                outfile.write(block)

        # 计算压缩结果
        comp_size = os.path.getsize(output_file) / 1024 / 1024
        save_size = orig_size - comp_size
        save_percent = (1 - comp_size / orig_size) * 100

        result_text = (f"✅ {os.path.basename(input_file)}\n"
                       f"  原始: {orig_size:.2f} MB → 压缩后: {comp_size:.2f} MB\n"
                       f"  节省: {save_size:.2f} MB ({save_percent:.1f}%)\n")
        print(result_text)
        return True, result_text

    except Exception as e:
        error_msg = f"❌ {os.path.basename(input_file)}: {str(e)}"
        print(error_msg)
        return False, error_msg


def get_output_filename(input_path, flag=COMPRESS_FLAG):
    """
    生成输出文件名：原文件名 + 标志 + 扩展名
    例如：test.wav → test_compressed.wav
    """
    dir_name = os.path.dirname(input_path)
    file_name = os.path.basename(input_path)
    name, ext = os.path.splitext(file_name)

    # 如果文件名已经包含标志，直接返回None（避免重复压缩）
    if flag in name:
        return None

    # 生成新文件名
    new_name = f"{name}{flag}{ext}"
    return os.path.join(dir_name, new_name)


# ------------------------ 单文件处理函数 ------------------------
def select_input_file():
    """选择输入音频文件"""
    file_path = filedialog.askopenfilename(
        title="选择音频文件",
        filetypes=[("WAV文件", "*.wav"), ("所有文件", "*.*")]
    )
    if file_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)
        # 自动生成输出文件名
        output_path = get_output_filename(file_path)
        if output_path:
            output_entry.delete(0, tk.END)
            output_entry.insert(0, output_path)


def select_output_file():
    """选择输出音频文件"""
    file_path = filedialog.asksaveasfilename(
        title="保存压缩后的音频",
        defaultextension=".wav",
        filetypes=[("WAV文件", "*.wav"), ("所有文件", "*.*")]
    )
    if file_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file_path)


def start_single_compression():
    """开始压缩单个音频文件"""
    # 获取输入输出路径
    input_file = input_entry.get().strip()
    output_file = output_entry.get().strip()

    # 验证路径
    if not input_file:
        messagebox.showerror("错误", "请选择输入音频文件！")
        return
    if not output_file:
        messagebox.showerror("错误", "请选择输出文件保存路径！")
        return
    if not os.path.exists(input_file):
        messagebox.showerror("错误", "输入文件不存在！")
        return

    # 检查是否已压缩过
    if COMPRESS_FLAG in os.path.basename(input_file):
        messagebox.warning("提示", "该文件已包含压缩标志，可能是已压缩过的文件！")
        if not messagebox.askyesno("确认", "是否继续压缩？"):
            return

    # 获取参数
    mono = mono_var.get()
    sample_rate = int(sample_rate_var.get())
    subtype = subtype_var.get()

    # 禁用按钮防止重复点击
    single_compress_btn.config(state=tk.DISABLED)
    batch_compress_btn.config(state=tk.DISABLED)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "正在压缩中...\n（超大文件会分块处理，耐心等待）\n")
    root.update()

    # 执行压缩
    success, msg = compress_audio_smaller(input_file, output_file, mono, sample_rate, subtype)

    # 更新结果显示
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, msg)

    # 提示结果
    if success:
        messagebox.showinfo("成功", "音频压缩完成！")
    else:
        messagebox.showerror("失败", msg)

    # 恢复按钮状态
    single_compress_btn.config(state=tk.NORMAL)
    batch_compress_btn.config(state=tk.NORMAL)


# ------------------------ 批量处理函数 ------------------------
def select_batch_folder():
    """选择批量处理的文件夹"""
    folder_path = filedialog.askdirectory(title="选择包含音频文件的文件夹")
    if folder_path:
        batch_entry.delete(0, tk.END)
        batch_entry.insert(0, folder_path)


def start_batch_compression():
    """批量压缩文件夹内的所有音频文件"""
    # 获取文件夹路径
    folder_path = batch_entry.get().strip()
    if not folder_path or not os.path.isdir(folder_path):
        messagebox.showerror("错误", "请选择有效的文件夹！")
        return

    # 获取参数
    mono = mono_var.get()
    sample_rate = int(sample_rate_var.get())
    subtype = subtype_var.get()

    # 查找文件夹内的所有WAV文件
    audio_files = glob.glob(os.path.join(folder_path, "*.wav"))
    if not audio_files:
        messagebox.warning("提示", "文件夹内未找到WAV音频文件！")
        return

    # 禁用按钮
    single_compress_btn.config(state=tk.DISABLED)
    batch_compress_btn.config(state=tk.DISABLED)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"开始批量处理，共找到 {len(audio_files)} 个音频文件...\n\n")
    root.update()

    # 统计结果
    success_count = 0
    fail_count = 0
    skip_count = 0
    result_log = []

    # 遍历处理每个文件
    for input_file in audio_files:
        # 生成输出文件名
        output_file = get_output_filename(input_file)
        if not output_file:
            # 已包含压缩标志，跳过
            skip_count += 1
            skip_msg = f"⏭️ 跳过 {os.path.basename(input_file)}（已包含压缩标志）"
            result_log.append(skip_msg)
            continue

        # 执行压缩
        success, msg = compress_audio_smaller(input_file, output_file, mono, sample_rate, subtype)
        result_log.append(msg)
        if success:
            success_count += 1
        else:
            fail_count += 1

        # 实时更新结果
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "\n".join(result_log))
        result_text.see(tk.END)  # 滚动到最后
        root.update()

    # 生成汇总报告
    summary = f"""
==================== 批量处理完成 ====================
✅ 成功: {success_count} 个
❌ 失败: {fail_count} 个
⏭️ 跳过: {skip_count} 个
=====================================================
提示：已压缩文件命名包含「{COMPRESS_FLAG}」标志，避免重复压缩
"""
    result_log.append(summary)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "\n".join(result_log))

    # 提示结果
    messagebox.showinfo("批量处理完成",
                        f"✅ 成功: {success_count} 个\n❌ 失败: {fail_count} 个\n⏭️ 跳过: {skip_count} 个")

    # 恢复按钮状态
    single_compress_btn.config(state=tk.NORMAL)
    batch_compress_btn.config(state=tk.NORMAL)


# ------------------------ UI界面 ------------------------
# 创建主窗口
root = tk.Tk()
root.title("音频压缩工具（支持批量+超大文件）")
root.geometry("700x650")
root.resizable(False, False)

# ========== 单文件处理区域 ==========
single_frame = ttk.LabelFrame(root, text="单文件处理")
single_frame.pack(fill=tk.X, padx=20, pady=10)

# 输入文件
input_entry = ttk.Entry(single_frame)
input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
input_btn = ttk.Button(single_frame, text="选择文件", command=select_input_file)
input_btn.pack(side=tk.LEFT, padx=5, pady=10)

# 输出文件
output_entry = ttk.Entry(single_frame)
output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
output_btn = ttk.Button(single_frame, text="保存路径", command=select_output_file)
output_btn.pack(side=tk.LEFT, padx=5, pady=10)

# ========== 批量处理区域 ==========
batch_frame = ttk.LabelFrame(root, text="批量处理")
batch_frame.pack(fill=tk.X, padx=20, pady=10)

batch_entry = ttk.Entry(batch_frame)
batch_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
batch_btn = ttk.Button(batch_frame, text="选择文件夹", command=select_batch_folder)
batch_btn.pack(side=tk.LEFT, padx=5, pady=10)

# ========== 参数设置区域 ==========
param_frame = ttk.LabelFrame(root, text="压缩参数（单/批量通用）")
param_frame.pack(fill=tk.X, padx=20, pady=10)

# 单声道选项
mono_var = tk.BooleanVar(value=True)
mono_check = ttk.Checkbutton(param_frame, text="转为单声道", variable=mono_var)
mono_check.pack(side=tk.LEFT, padx=20, pady=10)

# 采样率选择
sample_rate_var = tk.StringVar(value="16000")
sample_rate_label = ttk.Label(param_frame, text="采样率:")
sample_rate_label.pack(side=tk.LEFT, padx=(20, 5), pady=10)
sample_rate_combo = ttk.Combobox(param_frame, textvariable=sample_rate_var,
                                 values=["8000", "16000", "22050", "44100"], width=10)
sample_rate_combo.pack(side=tk.LEFT, padx=5, pady=10)

# 位深选择
subtype_var = tk.StringVar(value="PCM_16")
subtype_label = ttk.Label(param_frame, text="位深:")
subtype_label.pack(side=tk.LEFT, padx=(20, 5), pady=10)
subtype_combo = ttk.Combobox(param_frame, textvariable=subtype_var,
                             values=["PCM_16", "PCM_8"], width=10)
subtype_combo.pack(side=tk.LEFT, padx=5, pady=10)

# ========== 操作按钮 ==========
btn_frame = ttk.Frame(root)
btn_frame.pack(pady=10)

single_compress_btn = ttk.Button(btn_frame, text="压缩单个文件", command=start_single_compression)
single_compress_btn.pack(side=tk.LEFT, padx=20)

batch_compress_btn = ttk.Button(btn_frame, text="批量压缩文件夹", command=start_batch_compression)
batch_compress_btn.pack(side=tk.LEFT, padx=20)

# ========== 结果显示区域 ==========
result_frame = ttk.LabelFrame(root, text="处理结果")
result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

result_text = tk.Text(result_frame, height=12, wrap=tk.WORD)
result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# 运行主循环
if __name__ == "__main__":
    root.mainloop()