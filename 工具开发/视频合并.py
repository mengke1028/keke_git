import subprocess

def merge_mp4_files(file_list, output_file):
    # 创建一个临时文件来存储文件列表
    with open("filelist.txt", "w") as f:
        for file in file_list:
            f.write(f"file '{file}'\n")

    # 构建 ffmpeg 命令
    command = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", "filelist.txt",
        "-c", "copy",
        output_file
    ]

    # 执行命令
    try:
        subprocess.run(command, check=True)
        print(f"Video files merged successfully: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while merging video files: {e}")

# 示例文件列表
file_list = ["video1.mp4", "video2.mp4", "video3.mp4"]
output_file = "merged_video.mp4"

# 调用函数合并视频文件
merge_mp4_files(file_list, output_file)
