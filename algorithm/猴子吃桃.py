"""
    一堆桃子 猴子第一天吃了一半加一个 第二天又吃了剩下的一半加1个 第十天还剩一个桃子 问总共有多少桃子
"""


def result(n):
    if n == 1:
        return 1
    return (result(n - 1) + 1) * 2


if __name__ == '__main__':
    print(result(10))
