import os
import time
import m3u8
import requests
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
import subprocess


def parse_m3u8(url):
    """解析 m3u8 链接，返回 ts 文件列表"""
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"请求失败: {response.status_code}")
            return []

        m3u8_obj = m3u8.loads(response.text)
        base_url = url.rsplit('/', 1)[0] + '/'

        ts_files = []
        if m3u8_obj.is_variant:
            # 多层级 m3u8，选择第一个可用的流
            playlist_url = urljoin(base_url, m3u8_obj.playlists[0].uri)
            print(f"检测到多层级 m3u8，使用: {playlist_url}")
            return parse_m3u8(playlist_url)
        else:
            # 单层 m3u8，直接获取 ts 文件
            for segment in m3u8_obj.segments:
                ts_url = urljoin(base_url, segment.uri)
                ts_files.append(ts_url)
            return ts_files

    except Exception as e:
        print(f"解析 m3u8 失败: {e}")
        return []


def download_ts(url, output_dir, retry_times=3):
    """下载单个 ts 文件"""
    try:
        filename = url.split('/')[-1]
        output_path = os.path.join(output_dir, filename)

        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            return filename

        for i in range(retry_times):
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                return filename
            else:
                print(f"下载失败 ({response.status_code})，重试 {i + 1}/{retry_times}: {url}")
                time.sleep(1)

        print(f"下载失败: {url}")
        return None

    except Exception as e:
        print(f"下载出错: {e}")
        return None


def merge_ts_files(ts_files, output_dir, output_filename):
    """合并所有 ts 文件"""
    try:
        # 按文件名排序
        ts_files.sort()

        # 生成合并列表文件
        list_file = os.path.join(output_dir, 'filelist.txt')
        with open(list_file, 'w') as f:
            for ts_file in ts_files:
                f.write(f"file '{ts_file}'\n")

        # 合并文件
        output_path = os.path.join(output_dir, output_filename)
        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', list_file,
            '-c', 'copy',
            output_path
        ]

        print("正在合并视频片段...")
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"视频合并完成: {output_path}")

        # 清理临时文件
        os.remove(list_file)

    except Exception as e:
        print(f"合并失败: {e}")


def main(M3U8_URL):
    # 直接写死的配置参数
    OUTPUT_FILE = "output.mp4"
    DOWNLOAD_THREADS = 10
    TEMP_DIR = "downloads"

    # 创建临时目录
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    # 解析 m3u8 文件
    print("正在解析 m3u8 文件...")
    ts_files = parse_m3u8(M3U8_URL)

    if not ts_files:
        print("未找到视频片段，下载终止")
        return

    print(f"找到 {len(ts_files)} 个视频片段")

    # 下载所有 ts 文件
    print("开始下载视频片段...")
    downloaded_files = []

    with ThreadPoolExecutor(max_workers=DOWNLOAD_THREADS) as executor:
        results = list(executor.map(lambda x: download_ts(x, TEMP_DIR), ts_files))
        downloaded_files = [r for r in results if r]

    print(f"成功下载 {len(downloaded_files)}/{len(ts_files)} 个片段")

    # 合并文件
    if downloaded_files:
        merge_ts_files(downloaded_files, TEMP_DIR, OUTPUT_FILE)
    else:
        print("没有可合并的视频片段")


if __name__ == "__main__":
    M3U8_URL = "https://example.com/path/to/your/video.m3u8"  # <-- 修改为你的 m3u8 URL
    main(M3U8_URL)