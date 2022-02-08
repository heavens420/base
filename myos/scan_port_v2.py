from os import system

'''
Warning: inverse host lookup failed for 81.68.241.197: h_errno 11004: NO_DATA        
jing.tk [81.68.241.197] 50000 (?) open


Warning: inverse host lookup failed for 81.68.241.197: h_errno 11004: NO_DATA        
jing.tk [81.68.241.197] 8881 (?): TIMEDOUT 
'''


def promote():
    try:
        host, port = input("请输入 要测试的IP和端口 用空格隔开 eg:baidu.com 80\n").split(" ")
        return host, port
    except Exception:
        print("格式错误！")


def scan_port():
    host, port = promote()

    tcp_cmd = "nc -zw 3 " + host + " " + port
    udp_cmd = "nc -zuw 3 " + host + " " + port

    tcp_status = system(tcp_cmd)
    print()

    if tcp_status == 0:
        print(f"连接{host} {port}/TCP端口成功")
    else:
        print(f"连接{host}的{port}/TCP端口失败")

    udp_status = system(udp_cmd)
    print()

    if udp_status == 0:
        print(f"连接{host} {port}/DUP端口成功")
    else:
        print(f"连接{host} {port}/UDP端口失败")

    print()


while 1:
    try:
        scan_port()
    except Exception:
        # print("格式有误！")
        pass
