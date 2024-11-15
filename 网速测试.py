import speedtest
import socket


def test_internet_speed():
    # 创建一个Speedtest对象
    st = speedtest.Speedtest()

    print("正在查找最佳服务器...")
    st.get_best_server()

    print("开始下载速度测试...")
    download_speed = st.download() / 10 ** 6  # 将结果转换为Mbps
    print(f"下载速度: {download_speed:.2f} Mbps")

    print("开始上传速度测试...")
    upload_speed = st.upload() / 10 ** 6  # 将结果转换为Mbps
    print(f"上传速度: {upload_speed:.2f} Mbps")


def get_local_ip():
    try:
        # 创建一个socket对象
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 连接到一个已知的外部服务器，这里使用Google的DNS服务器
        s.connect(('8.8.8.8', 80))
        # 获取本地IP地址
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return "无法获取IP地址: " + str(e)


if __name__ == "__main__":
    # test_internet_speed()
    print("本机IP地址:", get_local_ip())
