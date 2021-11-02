import os
import re

protocol = input("请输入端口协议(默认tcp)：tcp/udp 例:tcp\n")
host, port = input("请输入 要测试的IP和端口 用空格隔开\n").split(" ")
tcp_cmd = "nc -zvw 2 " + host + " " + port
udp_cmd = "nc -zuvw 2 " + host + " " + port
result = 100
if protocol != "udp":
    rep = os.system(tcp_cmd)
else:
    rep = os.system(udp_cmd)
# print(rep.read())
if rep == 0:
    print(f"{port}端口开放")
else:
    print(f"{port}端口关闭")

while 1:
    pass
