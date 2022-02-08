from os import system

'''
Warning: inverse host lookup failed for 81.68.241.197: h_errno 11004: NO_DATA        
jing.tk [81.68.241.197] 50000 (?) open


Warning: inverse host lookup failed for 81.68.241.197: h_errno 11004: NO_DATA        
jing.tk [81.68.241.197] 8881 (?): TIMEDOUT 
'''


def promote():
    protocol = input("请输入端口协议(默认tcp)：tcp/udp 例:tcp\n")
    host, port = input("请输入 要测试的IP和端口 用空格隔开 eg:baidu.com 80\n").split(" ")
    return protocol, host, port


def scan_port():
    protocol, host, port = promote()
    tcp_cmd = "nc -zw 3 " + host + " " + port
    udp_cmd = "nc -zuw 3 " + host + " " + port
    if protocol != "udp":
        rep = system(tcp_cmd)
    else:
        rep = system(udp_cmd)
    if rep == 0:
        print(f"{port}端口开放")
    else:
        print(f"{port}端口关闭")
    print()


while 1:
    scan_port()
