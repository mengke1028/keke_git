# -*- coding: utf-8 -*-
# Keke.Meng  2025/6/17
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import requests
import json
import os
import re
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import time
import queue


class BilibiliVideoDownloader:
    """B站视频信息获取与下载工具"""

    def __init__(self, log_callback=None, progress_callback=None):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://www.bilibili.com/",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://www.bilibili.com"
        })
        self.video_info = None
        self.log_callback = log_callback
        self.progress_callback = progress_callback
        self.stop_flag = False

    def log(self, message):
        """日志输出回调"""
        if self.log_callback:
            self.log_callback(message)
        else:
            print(message)

    def update_progress(self, total, current, message=None):
        """更新进度回调"""
        if self.progress_callback:
            self.progress_callback(total, current, message)

    def get_bilibili_video_info(self, bvid):
        """获取B站视频信息"""
        self.log(f"正在获取视频 {bvid} 的信息...")
        self.update_progress(100, 0, "获取视频信息中...")
        url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"

        try:
            response = self.session.get(url)
            response.raise_for_status()  # 检查请求是否成功
            data = response.json()
            # print(data)

            if data["code"] == 0:
                self.video_info = data["data"]
                self._print_video_info()
                self.update_progress(100, 100, "获取视频信息完成")
                return self.video_info
            else:
                self.log(f"请求失败，错误码: {data['code']}，错误信息: {data['message']}")
                self.update_progress(100, 100, f"获取视频信息失败: {data['message']}")
                return None

        except requests.exceptions.RequestException as e:
            self.log(f"网络请求异常: {e}")
            self.update_progress(100, 100, f"网络请求异常: {e}")
            return None
        except json.JSONDecodeError:
            self.log("解析JSON响应失败")
            self.update_progress(100, 100, "解析JSON响应失败")
            return None
        except Exception as e:
            self.log(f"发生未知错误: {e}")
            self.update_progress(100, 100, f"发生未知错误: {e}")
            return None

    def _print_video_info(self):
        """打印视频信息"""
        if not self.video_info:
            return

        info = self.video_info
        self.log("\n===== 视频信息 =====")
        self.log(f"标题: {info['title']}")
        self.log(f"UP主: {info['owner']['name']} ({info['owner']['mid']})")
        self.log(f"分区: {info['tname']}")
        self.log(f"发布时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(info['pubdate']))}")
        self.log(f"播放量: {self._format_number(info['stat']['view'])}")
        self.log(f"弹幕数: {self._format_number(info['stat']['danmaku'])}")
        self.log(f"点赞数: {self._format_number(info['stat']['like'])}")
        self.log(f"投币数: {self._format_number(info['stat']['coin'])}")
        self.log(f"收藏数: {self._format_number(info['stat']['favorite'])}")
        self.log(f"分享数: {self._format_number(info['stat']['share'])}")
        self.log(f"简介: {info['desc'].strip()[:200]}...")  # 截取前200个字符

    def _format_number(self, num):
        """格式化数字显示"""
        if num >= 10000:
            return f"{num / 10000:.2f}万"
        return str(num)

    def get_video_url(self, bvid=None, cid=None, quality=116):
        """
        获取视频播放地址
        quality参数说明:
        116: 高清1080P60(需要大会员)
        80: 高清1080P
        64: 高清720P
        32: 清晰480P
        16: 流畅360P
        """
        self.log("正在获取视频下载地址...")
        self.update_progress(100, 0, "获取视频下载地址中...")

        if not self.video_info and not (bvid and cid):
            self.log("请先获取视频信息或提供bvid和cid")
            self.update_progress(100, 100, "请先获取视频信息")
            return None


        if not cid:
            cid = self.video_info['cid']

        if not bvid:
            bvid = self.video_info['bvid']

        url = "https://api.bilibili.com/x/player/playurl"
        params = {
            "bvid": bvid,
            "cid": cid,
            "fnval": 16,  # 允许下载
            "fnval": 0,  # 关闭dash模式
            "fourk": 1,  # 支持4K
            "qn": quality  # 视频质量
        }

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if data["code"] == 0:
                if 'durl' in data['data'] and data['data']['durl']:
                    # 普通视频流
                    self.log(f"成功获取普通视频流，共{len(data['data']['durl'])}段")
                    self.update_progress(100, 100, "获取视频下载地址完成")
                    return [{"url": item["url"], "size": item["size"]} for item in data['data']['durl']]
                elif 'dash' in data['data']:
                    # dash格式视频流(高清/高帧率)
                    self.log("成功获取DASH格式视频流(包含独立视频和音频)")
                    self.update_progress(100, 100, "获取视频下载地址完成")
                    video_urls = [{"url": url, "size": 0} for url in data['data']['dash']['video'][0]['baseUrl']]
                    audio_urls = [{"url": url, "size": 0} for url in data['data']['dash']['audio'][0]['baseUrl']]
                    return video_urls, audio_urls
                else:
                    self.log("未找到可用的视频链接")
                    self.update_progress(100, 100, "未找到可用的视频链接")
                    return None
            else:
                self.log(f"获取视频链接失败，错误码: {data['code']}，错误信息: {data['message']}")
                self.update_progress(100, 100, f"获取视频链接失败: {data['message']}")
                return None

        except Exception as e:
            self.log(f"获取视频链接异常: {e}")
            self.update_progress(100, 100, f"获取视频链接异常: {e}")
            return None

    def download_video(self, video_urls, output_dir=".", i=0 ,max_workers=5, only_audio=False):
        """下载视频或音频文件"""
        if not self.video_info:
            self.log("请先获取视频信息")
            self.update_progress(100, 100, "请先获取视频信息")
            return False

        # 创建输出目录
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            self.log(f"创建目录: {output_dir}")

        # 生成文件名(去除非法字符)
        title = re.sub(r'[\\/:*?"<>|]', '_', self.video_info['pages'][i]['part'])

        if only_audio:
            self.log(f"准备下载音频: {title}")
            output_path = os.path.join(output_dir, f"{title}.mp3")  # MP3格式
        else:
            self.log(f"准备下载视频: {title}")
            output_path = os.path.join(output_dir, f"{title}.mp4")  # MP4格式

        self.log(f"保存路径: {output_path}")

        # 估计总大小用于进度条
        total_size = 0

        if isinstance(video_urls, tuple):
            # dash格式(视频+音频)
            video_urls, audio_urls = video_urls

            if only_audio:
                # 只下载音频
                audio_path = os.path.join(output_dir, f"{title}.m4a")

                # 尝试获取音频的总大小
                for part in audio_urls:
                    if 'size' in part:
                        total_size += part['size']

                self.log(f"\n开始下载音频...")
                self.update_progress(total_size, 0, "开始下载音频...")
                downloaded_size = self._download_parts(audio_urls, audio_path, max_workers)

                if self.stop_flag:
                    self.log("下载已取消")
                    return False

                if downloaded_size >= 0:
                    self.log("\n开始转换音频格式...")
                    self.update_progress(total_size, downloaded_size, "开始转换音频格式...")
                    success = self._convert_to_mp3(audio_path, output_path)
                    if success:
                        # 转换成功后删除临时文件
                        if os.path.exists(audio_path):
                            os.remove(audio_path)
                        self.log(f"音频已成功下载并转换为MP3: {output_path}")
                        self.update_progress(total_size, total_size, "音频下载完成")
                    return success
                else:
                    self.update_progress(total_size, total_size, "音频下载失败")
                    return False
            else:
                # 下载视频和音频
                video_path = os.path.join(output_dir, f"{title}_video.mp4")
                audio_path = os.path.join(output_dir, f"{title}_audio.m4a")

                # 尝试获取视频和音频的总大小
                for part in video_urls:
                    if 'size' in part:
                        total_size += part['size']
                for part in audio_urls:
                    if 'size' in part:
                        total_size += part['size']

                self.log(f"\n开始下载视频流...")
                self.update_progress(total_size, 0, "开始下载视频流...")
                downloaded_size = self._download_parts(video_urls, video_path, max_workers)

                if self.stop_flag:
                    self.log("下载已取消")
                    return False

                if downloaded_size >= 0:
                    self.log(f"\n开始下载音频流...")
                    self.update_progress(total_size, downloaded_size, "开始下载音频流...")
                    downloaded_size += self._download_parts(audio_urls, audio_path, max_workers)

                if self.stop_flag:
                    self.log("下载已取消")
                    return False

                if downloaded_size >= 0:
                    self.log("\n开始合并视频和音频...")
                    self.update_progress(total_size, downloaded_size, "开始合并视频和音频...")
                    success = self._merge_video_audio(video_path, audio_path, output_path)
                    if success:
                        # 合并成功后删除临时文件
                        if os.path.exists(video_path):
                            os.remove(video_path)
                        if os.path.exists(audio_path):
                            os.remove(audio_path)
                        self.log(f"视频已成功下载到: {output_path}")
                        self.update_progress(total_size, total_size, "视频下载完成")
                    return success
                else:
                    self.update_progress(total_size, total_size, "视频下载失败")
                    return False
        else:
            # 普通格式
            if only_audio:
                self.log("警告: 此视频只有普通格式，无法单独提取音频。将下载完整视频。")
                self.update_progress(100, 0, "警告: 此视频只有普通格式，无法单独提取音频。将下载完整视频。")
                # 尝试获取总大小
                for part in video_urls:
                    if 'size' in part:
                        total_size += part['size']

                self.log(f"\n开始下载视频...")
                self.update_progress(total_size, 0, "开始下载视频...")
                success = self._download_parts(video_urls, output_path, max_workers)

                if success:
                    self.log(f"视频已成功下载到: {output_path}")
                    self.update_progress(total_size, total_size, "视频下载完成")
                return success
            else:
                # 尝试获取总大小
                for part in video_urls:
                    if 'size' in part:
                        total_size += part['size']

                self.log(f"\n开始下载视频...")
                self.update_progress(total_size, 0, "开始下载视频...")
                success = self._download_parts(video_urls, output_path, max_workers)

                if success:
                    self.log(f"视频已成功下载到: {output_path}")
                    self.update_progress(total_size, total_size, "视频下载完成")
                    return True
                else:
                    self.update_progress(total_size, total_size, "视频下载失败")
                    return False

    def stop_download(self):
        """停止下载"""
        self.stop_flag = True
        self.log("正在停止下载...")

    def _download_parts(self, parts, output_path, max_workers):
        """下载视频分段并合并，返回已下载的总大小"""
        if self.stop_flag:
            return -1

        total_downloaded = 0

        if len(parts) == 1:
            # 只有一个分段，直接下载
            size = self._download_single_part(parts[0]["url"], output_path)
            return size if size >= 0 else -1

        # 多个分段，分段下载后合并
        temp_dir = os.path.dirname(output_path)
        part_paths = []

        try:
            def download_part(part_info, index):
                nonlocal total_downloaded
                if self.stop_flag:
                    return False

                part_url = part_info["url"]
                part_size = part_info.get("size", 0)
                part_path = os.path.join(temp_dir, f"temp_{index}.ts")

                self.log(f"开始下载分段 {index + 1}/{len(parts)}")
                size = self._download_single_part(part_url, part_path)

                if size >= 0:
                    part_paths.append((index, part_path))
                    total_downloaded += size
                    return True
                return False

            # 多线程下载分段
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                results = list(executor.map(lambda x: download_part(*x), enumerate(parts)))

            # 检查是否所有分段都下载成功或已停止
            if self.stop_flag:
                return -1

            if not all(results):
                self.log("部分分段下载失败")
                return -1

            # 按索引排序分段
            part_paths.sort(key=lambda x: x[0])

            # 合并分段
            self.log("开始合并分段...")
            self._merge_video_parts(part_paths, output_path)

            return total_downloaded

        except Exception as e:
            self.log(f"下载分段时出错: {e}")
            # 清理临时文件
            for _, part_path in part_paths:
                if os.path.exists(part_path):
                    os.remove(part_path)
            return -1

    def _download_single_part(self, url, output_path):
        """下载单个文件，返回下载的大小"""
        if self.stop_flag:
            return -1

        def convert_size(size_bytes):
            units = ['B', 'KB', 'MB', 'GB', 'TB']
            unit_index = 0
            while size_bytes >= 1024 and unit_index < len(units) - 1:
                size_bytes /= 1024
                unit_index += 1
            return f"{size_bytes:.2f} {units[unit_index]}"
        try:
            # 如果文件已存在，则获取其大小
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                self.log(f"文件已存在: {output_path}，大小: {convert_size(file_size)}")
                return file_size

            # 开始下载
            self.log(f"开始下载: {os.path.basename(output_path)}")

            with self.session.get(url, stream=True) as response:
                response.raise_for_status()

                # 获取文件大小用于进度条
                total_size = int(response.headers.get('Content-Length', 0))
                block_size = 1024  # 1 KB
                downloaded_size = 0

                with open(output_path, 'wb') as file:
                    for data in response.iter_content(block_size):
                        if self.stop_flag:
                            return -1

                        file.write(data)
                        downloaded_size += len(data)

                        # 每下载1MB更新一次进度
                        if downloaded_size % (1024 * 1024) < block_size or downloaded_size == total_size:
                            progress_msg = f"下载进度: {downloaded_size / 1024 / 1024:.2f}MB / {total_size / 1024 / 1024:.2f}MB"
                            # self.log(progress_msg)
                            self.update_progress(total_size, downloaded_size, progress_msg)

            self.log(f"下载完成: {os.path.basename(output_path)}")
            return downloaded_size

        except Exception as e:
            self.log(f"下载文件时出错: {e}")
            # 删除不完整的文件
            if os.path.exists(output_path):
                os.remove(output_path)
            return -1

    def _merge_video_parts(self, part_paths, output_path):
        """合并多个视频片段为一个完整视频"""
        # 使用ffmpeg的concat demuxer方法，更可靠
        concat_file = os.path.join(os.path.dirname(output_path), "concat_list.txt")

        try:
            # 创建合并列表文件
            with open(concat_file, 'w', encoding='utf-8') as f:
                for _, part_path in part_paths:
                    # 转义文件路径中的特殊字符
                    path = part_path.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')
                    f.write(f"file '{path}'\n")

            # 使用moviepy进行合并(需要安装moviepy和ffmpeg)
            try:
                from moviepy.editor import VideoFileClip, concatenate_videoclips
                clips = [VideoFileClip(part_path) for _, part_path in part_paths]
                final_clip = concatenate_videoclips(clips)
                final_clip.write_videofile(
                    output_path,
                    codec="libx264",
                    audio_codec="aac",
                    verbose=False,
                    logger=None
                )
                # 关闭clip对象释放资源
                for clip in clips:
                    clip.close()
                final_clip.close()
                self.log("视频片段合并完成")
            except ImportError:
                # 如果没有moviepy，尝试使用系统ffmpeg命令
                import subprocess
                cmd = [
                    'ffmpeg',
                    '-f', 'concat',
                    '-safe', '0',
                    '-i', concat_file,
                    '-c', 'copy',
                    output_path
                ]
                self.log("正在使用系统ffmpeg合并视频片段...")
                result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode != 0:
                    self.log(f"ffmpeg合并失败: {result.stderr.decode('utf-8')}")
                    raise Exception("视频合并失败")
                self.log("视频片段合并完成")

        except Exception as e:
            self.log(f"合并视频片段时出错: {e}")
            raise
        finally:
            # 删除合并列表文件和临时文件
            if os.path.exists(concat_file):
                os.remove(concat_file)
            for _, part_path in part_paths:
                if os.path.exists(part_path):
                    os.remove(part_path)

    def _merge_video_audio(self, video_path, audio_path, output_path):
        """合并视频和音频文件"""
        try:
            # 使用moviepy合并视频和音频
            from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip

            self.log("正在加载视频和音频文件...")
            video = VideoFileClip(video_path)
            audio = AudioFileClip(audio_path)

            # 设置视频的音频
            self.log("正在合并视频和音频...")
            final_clip = video.set_audio(audio)

            # 保存合并后的文件为MP4格式
            self.log("正在保存合并后的文件...")
            final_clip.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                verbose=False,
                logger=None
            )

            # 关闭clip对象释放资源
            video.close()
            audio.close()
            final_clip.close()

            self.log("视频和音频合并完成")
            return True

        except ImportError:
            self.log("警告: 未安装moviepy库，无法合并视频和音频。请手动合并。")
            self.log(f"视频文件已保存到: {video_path}")
            self.log(f"音频文件已保存到: {audio_path}")
            return False
        except Exception as e:
            self.log(f"合并视频和音频时出错: {e}")
            return False

    def _convert_to_mp3(self, input_path, output_path):
        """将音频文件转换为MP3格式"""
        try:
            from moviepy.editor import AudioFileClip

            self.log(f"正在将音频转换为MP3格式...")
            audio = AudioFileClip(input_path)
            audio.write_audiofile(
                output_path,
                codec="mp3",
                verbose=False,
                logger=None
            )
            audio.close()
            self.log(f"音频转换完成: {output_path}")
            return True
        except ImportError:
            self.log("警告: 未安装moviepy库，无法转换音频格式。请手动转换。")
            self.log(f"原始音频文件已保存到: {input_path}")
            return False
        except Exception as e:
            self.log(f"转换音频格式时出错: {e}")
            return False


class BilibiliDownloaderGUI:
    """B站视频下载器图形界面"""

    def __init__(self, root):
        self.root = root
        self.root.title("小鱼干B站视频下载器")
        self.root.geometry("800x650")
        self.root.resizable(True, True)

        # 设置中文字体支持
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("SimHei", 10))
        self.style.configure("TButton", font=("SimHei", 10))
        self.style.configure("TEntry", font=("SimHei", 10))

        # 创建下载器实例
        self.downloader = BilibiliVideoDownloader(self.log_message, self.update_progress)
        self.download_thread = None
        self.log_queue = queue.Queue()
        self.progress_queue = queue.Queue()

        # 创建UI组件
        self.create_widgets()

        # 启动日志和进度处理线程
        self.root.after(100, self.process_log_queue)
        self.root.after(100, self.process_progress_queue)

    def create_widgets(self):
        """创建UI组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # BVID输入区域
        bvid_frame = ttk.LabelFrame(main_frame, text="视频信息", padding="10")
        bvid_frame.pack(fill=tk.X, pady=5)

        ttk.Label(bvid_frame, text="BVID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.bvid_entry = ttk.Entry(bvid_frame, width=40)
        self.bvid_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        self.bvid_entry.insert(0, "BV1jxKozWEbc")  # BV1iKwCe1Ebj

        self.get_info_btn = ttk.Button(bvid_frame, text="获取视频信息", command=self.get_video_info)
        self.get_info_btn.grid(row=0, column=2, sticky=tk.W, pady=5, padx=5)

        # 下载设置区域
        download_frame = ttk.LabelFrame(main_frame, text="下载设置", padding="10")
        download_frame.pack(fill=tk.X, pady=5)

        ttk.Label(download_frame, text="保存路径:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.save_path_var = tk.StringVar(value="./videos")
        self.save_path_entry = ttk.Entry(download_frame, textvariable=self.save_path_var, width=40)
        self.save_path_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)

        self.browse_btn = ttk.Button(download_frame, text="浏览...", command=self.browse_save_path)
        self.browse_btn.grid(row=0, column=2, sticky=tk.W, pady=5, padx=5)

        ttk.Label(download_frame, text="视频质量:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.quality_var = tk.StringVar(value="1080P")
        quality_combo = ttk.Combobox(download_frame, textvariable=self.quality_var, state="readonly", width=10)
        quality_combo['values'] = ("1080P60", "1080P", "720P", "480P", "360P")
        quality_combo.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)

        # 下载类型选择
        ttk.Label(download_frame, text="下载类型:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.download_type_var = tk.IntVar(value=0)  # 0: 视频, 1: 音频
        video_radio = ttk.Radiobutton(download_frame, text="视频", variable=self.download_type_var, value=0)
        audio_radio = ttk.Radiobutton(download_frame, text="音频(MP3)", variable=self.download_type_var, value=1)
        video_radio.grid(row=2, column=1, sticky=tk.W, pady=5)
        audio_radio.grid(row=2, column=1, sticky=tk.E, pady=5, padx=50)

        # 下载控制按钮
        control_frame = ttk.Frame(download_frame)
        control_frame.grid(row=2, column=2, sticky=tk.W, pady=5)

        self.download_btn = ttk.Button(control_frame, text="开始下载", command=self.start_download)
        self.download_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = ttk.Button(control_frame, text="停止下载", command=self.stop_download, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        # 进度条区域
        progress_frame = ttk.LabelFrame(main_frame, text="下载进度", padding="10")
        progress_frame.pack(fill=tk.X, pady=5)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, length=100, mode='determinate')
        self.progress_bar.pack(fill=tk.X, expand=True, pady=5)

        self.progress_label = ttk.Label(progress_frame, text="就绪")
        self.progress_label.pack(anchor=tk.W, pady=2)

        # 日志显示区域
        log_frame = ttk.LabelFrame(main_frame, text="下载日志", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, width=70, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)

        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def log_message(self, message):
        """将消息添加到日志队列"""
        self.log_queue.put(message)

    def update_progress(self, total, current, message=None):
        """将进度更新添加到进度队列"""
        self.progress_queue.put((total, current, message))

    def process_log_queue(self):
        """处理日志队列中的消息"""
        while not self.log_queue.empty():
            try:
                message = self.log_queue.get_nowait()
                self.log_text.config(state=tk.NORMAL)
                self.log_text.insert(tk.END, message + "\n")
                self.log_text.see(tk.END)
                self.log_text.config(state=tk.DISABLED)
            except queue.Empty:
                pass
        self.root.after(100, self.process_log_queue)

    def process_progress_queue(self):
        """处理进度队列中的更新"""
        while not self.progress_queue.empty():
            try:
                total, current, message = self.progress_queue.get_nowait()

                # 计算百分比
                percent = 100.0
                if total > 0:
                    percent = min(100.0, (float(current) / float(total)) * 100.0)

                # 更新进度条和标签
                self.progress_var.set(percent)
                if message:
                    self.progress_label.config(text=message)
                else:
                    self.progress_label.config(text=f"进度: {percent:.1f}%")

            except queue.Empty:
                pass
        self.root.after(100, self.process_progress_queue)

    def get_video_info(self):
        """获取视频信息"""
        bvid = self.bvid_entry.get().strip()
        if not bvid:
            messagebox.showerror("错误", "请输入BVID")
            return

        self.status_var.set(f"正在获取视频 {bvid} 的信息...")
        self.get_info_btn.config(state=tk.DISABLED)
        self.download_btn.config(state=tk.DISABLED)

        # 清空日志
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)

        # 重置进度条
        self.progress_var.set(0)
        self.progress_label.config(text="获取视频信息中...")

        # 在新线程中获取视频信息
        self.download_thread = threading.Thread(target=self._get_video_info_thread, args=(bvid,))
        self.download_thread.daemon = True
        self.download_thread.start()

    def _get_video_info_thread(self, bvid):
        """获取视频信息的线程函数"""
        try:
            result = self.downloader.get_bilibili_video_info(bvid)
            if result:
                self.status_var.set(f"已获取视频 {bvid} 的信息")
                self.download_btn.config(state=tk.NORMAL)
            else:
                self.status_var.set(f"获取视频 {bvid} 的信息失败")
        except Exception as e:
            self.log_message(f"发生错误: {e}")
            self.status_var.set("获取视频信息时发生错误")
        finally:
            self.get_info_btn.config(state=tk.NORMAL)

    def browse_save_path(self):
        """浏览并选择保存路径"""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.save_path_var.set(folder_selected)

    def start_download(self):
        """开始下载视频或音频"""
        bvid = self.bvid_entry.get().strip()
        save_path = self.save_path_var.get().strip()

        if not bvid:
            messagebox.showerror("错误", "请输入BVID")
            return

        if not save_path:
            messagebox.showerror("错误", "请选择保存路径")
            return

        # 根据选择的质量设置对应的quality参数
        quality_map = {
            "1080P60": 116,
            "1080P": 80,
            "720P": 64,
            "480P": 32,
            "360P": 16
        }
        quality = quality_map[self.quality_var.get()]

        # 判断是下载视频还是音频
        only_audio = self.download_type_var.get() == 1

        self.status_var.set(f"正在准备{'下载音频' if only_audio else '下载视频'} {bvid}...")
        self.get_info_btn.config(state=tk.DISABLED)
        self.download_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.downloader.stop_flag = False

        # 重置进度条
        self.progress_var.set(0)
        self.progress_label.config(text=f"准备{'下载音频' if only_audio else '下载视频'}中...")

        # 在新线程中下载视频或音频
        self.download_thread = threading.Thread(target=self._download_thread,
                                                args=(bvid, save_path, quality, only_audio))
        self.download_thread.daemon = True
        self.download_thread.start()

    def _download_thread(self, bvid, save_path, quality, only_audio):
        """下载视频或音频的线程函数"""
        try:
            # 如果还没有获取视频信息，先获取信息
            if not self.downloader.video_info or self.downloader.video_info.get('bvid') != bvid:
                result = self.downloader.get_bilibili_video_info(bvid)
                if not result:
                    self.status_var.set(f"获取视频 {bvid} 的信息失败")
                    return
            result = self.downloader.get_bilibili_video_info(bvid)
            # 获取视频URL
            for i in range(len(result['pages'])):
                cid = result['pages'][i]['cid']
                video_urls = self.downloader.get_video_url(quality=quality, cid=cid)
                if not video_urls:
                    self.status_var.set(f"无法获取视频 {bvid} 的下载地址")
                    return

                # 开始下载
                if only_audio:
                    self.status_var.set(f"正在下载音频 {bvid}...")
                else:
                    self.status_var.set(f"正在下载视频 {bvid}...")

                success = self.downloader.download_video(video_urls, save_path,i, only_audio=only_audio)

                if success:
                    if only_audio:
                        self.status_var.set(f"音频 {bvid} 下载完成")
                    else:
                        self.status_var.set(f"视频 {bvid} 下载完成")
                else:
                    if only_audio:
                        self.status_var.set(f"音频 {bvid} 下载失败")
                    else:
                        self.status_var.set(f"视频 {bvid} 下载失败")

        except Exception as e:
            self.log_message(f"发生错误: {e}")
            if only_audio:
                self.status_var.set("下载音频时发生错误")
            else:
                self.status_var.set("下载视频时发生错误")
        finally:
            self.get_info_btn.config(state=tk.NORMAL)
            self.download_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)

    def stop_download(self):
        """停止下载"""
        self.status_var.set("正在停止下载...")
        self.downloader.stop_flag = True


if __name__ == "__main__":
    root = tk.Tk()
    app = BilibiliDownloaderGUI(root)
    root.mainloop()


"""

BV1jxKozWEbc
"""