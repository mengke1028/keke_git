# -*- coding: utf-8 -*-
# Keke.Meng  2025/3/14 11:32
import socket

# 创建一个 TCP/IP 套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接到服务端
server_address = ('localhost', 8888)
client_socket.connect(server_address)

try:
    # 发送指令到服务端
    command = 'ver'
    client_socket.sendall(command.encode('utf-8'))

    # 接收服务端返回的结果
    data = client_socket.recv(1024).decode('utf-8')
    print(f'大漠插件版本: {data}')
    #
    # # 发送另一个指令
    # command = 'find_color 0 0 1024 768 ff0000 0.9 0'
    # client_socket.sendall(command.encode('utf-8'))
    #
    # # 接收服务端返回的结果
    # data = client_socket.recv(1024).decode('utf-8')
    # print(f'查找颜色结果: {data}')

finally:
    # 关闭客户端连接
    client_socket.close()