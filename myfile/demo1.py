import os
import datetime
import re
from email.header import Header

def path_join():
    rs = os.path.join("qw", "23", "jfs", "iii")
    lst = [12, 3, 67, 8]
    res = os.path.join()

    print(rs)


def qtest_and():
    cmd = "echo 111 && echo 222"
    os.system(cmd)


def qtest_format_date():
    # print(datetime.datetime.strptime("%Y-%m-%d %H:%M:%S"))
    now = "20210909123456"
    now = datetime.datetime.strptime(now, "%Y%m%d%H%M%S")
    print(now)
    print(os.getcwd())


def qtest_os():
    print()
    # 获取当前文件目录
    print(os.getcwd())
    print()
    # 获取当前文件的绝对路径
    print(os.path.abspath(__file__))

    print(os.path.abspath("./demo1.py"))
    # 打印当前路径的上级目录
    print(os.path.dirname(os.getcwd()))
    os.chdir("../")
    print(os.getcwd())
    qtest_format_date()
    # os.system("mkdir hhhhhhhhhhhhh")
    # print(os.getcwd())


def qtest_group():
    sss = "2020120909344455.md5.txt"
    reg = r"(20\d{12}).md5.txt"
    match = re.compile(reg)
    result = re.search(reg, sss)
    print(result.group(1))
    if result:
        print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh" * 1)


def qtest_set():
    aa = (1, 2)
    bb = (3, 4)
    ss = set()
    ss.add(aa)
    ss.add(bb)
    lst = list(ss)
    print(lst[0][0])
    # print(ss[0])


def is_file():
    print(os.getcwd())
    sss = not os.path.isfile("demo1.py")
    print(sss)

if __name__ == '__main__':
    # sss = "1234567890"
    # ttt = sss[:3]
    # print(ttt)

    # print(os.system("ls"))

    lst = ['2332df','fsfsff']
    print(Header("".join(lst)))
    # test_and()
    # test_format_date()
    # qtest_os()
    # test_group()
    # test_set()

    # is_file()
