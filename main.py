import random


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def test_recurve(count):
    if count > 0:
        print(f'递归前{count}')
        test_recurve(count - 1)
        print(f'递归后{count}')


def test1():
    st = "http://{{URI}}/res/stn/staticroute/get?serialNo={{serialNo}}&deviceId={{deviceId}}&devicedIp={{devicedIp}}&destIP={{destIP}}&vpnName={{vpnName}}&extendInputParameterA={{extendInputParameterA}}&ex"
    ss = st.split("?")[0]
    print(ss)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    # test_recurve(3)
    # test1()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
