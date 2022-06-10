import sys


def split_test():
    ss = "jjj-kk-dsji-wedf"
    ind = ss.index("-") + 1
    print(ss[ind:])


def input_multi_line():
    for line in sys.stdin:
        a = line.split()
        print(a)


def input_test():
    while 1:
        aa = input().split()

        print(aa)


import sys

import sys


def convert():
    for line in sys.stdin:
        value = line.split()
        for item in value:
            result = 0
            num = len(item) - 3
            res = []
            for i in range(2, len(item)):
                if str(item[i]).upper() == 'A':
                    # item[i] = '10'
                    res.append(10)
                elif item[i].upper() == 'B':
                    #                     item[i] == '11'
                    res.append(11)
                elif item[i].upper() == 'C':
                    #                     item[i] == '12'
                    res.append(12)
                elif item[i].upper() == 'D':
                    #                     item[i] == '13'
                    res.append(13)
                elif item[i].upper() == 'E':
                    #                     item[i] == '14'
                    res.append(14)
                elif item[i].upper() == 'F':
                    #                     item[i] == '15'
                    res.append(15)
                else:
                    res.append(int(item[i]))

                result += res[i - 2] * pow(16, num)
                num -= 1
            print(result)


def charu():
    arr = [2, 5, 23, 1, 35, 6]

    for i in range(len(arr)):
        pre_index = i - 1
        current = arr[i]
        while pre_index >= 0 and arr[pre_index] > current:
            arr[pre_index] = arr[pre_index + 1]
            pre_index -= 1
        pre_index += 1
        arr[pre_index] = current


def remove_lst():
    lst = [1, 2, 3, 5, 6]
    kk = [2, 3]

    print(lst + kk)


def dict_order():
    hh = {12: 231, 13: 231, 14: 41, 15: 51, 16: 61}

    m = max(list(hh.values()))
    for it in hh:
        if hh.get(it) == m:
            print(it)
        # print(str(hh.get(it))+"   "+str(it))


# def test_jiequ():
#     while True:
#         try:
#             a, b = input().split()
#             print(a[:int(b)])
#
#         except:
#             break


def print_num(value):
    print(value % 10, end="")
    if value >= 10:
        print_num(value // 10)


def reverse_str(value):
    value = list(value)
    print(value[-1])
    if len(value) > 1:
        # 长度 > 1 即至少有两个元素 下面pop一个 再次递归时pop一个 正好两个 保证数组不会越界
        value.pop(-1)
        reverse_str(value)


def reverse_str2(value):
    if len(value) > 1:
        print(value[-1])
        value = value[:-1]
        reverse_str2(value)


def reverse_str3(value, index=-1):
    if index < len(value) - 1:
        index += 1
        reverse_str3(value, index)
        print(value[index])


def reverse_str4(value):
    i = 0

    def loop(i):
        if i < len(value):
            cur = i
            i += 1
            # 正序
            print(value[cur])
            loop(i)
            # 逆序
            print(value[cur])

    loop(i)


def GetResult(l):
    n = len(l)  # 传入list的长度
    dp = [1] * n  # dp[i]表示以第i个桩为结尾，最多走多少步，初始是1步（默认这个桩是跟它之前相比最矮的）
    res = 0  # 整个问题的结果
    for i in range(n):  # i表示第几个桩
        for j in range(i):  # j表示i前面的桩
            if l[i] > l[j]:  # 如果第i个桩前面有比它矮的（比如是j），
                # 且以第j个桩为结尾走的步数是最多的，
                # 步数就是dp[j]+1，加的这个1表示从第j个走1步到第i个桩；另一种就是dp[i],默认等于1，但是
                # 遍历j的过程可能会更新这个值，因此取上述两个结果中最大的那个值，表示第i个桩为结尾，
                # 最多走多少步
                dp[i] = max(dp[i], dp[j] + 1)
        res = max(res, dp[i])  # 到第i个桩时最多走几步
    return res



def fullpermutation(list):
    if list is None:
        return None
    if len(list) == 1:
        return [list]
    res = []
    pivot = list[0]
    remain = fullpermutation(list[1:])
    # print(remain)

# fullpermutation([1, 2, 3])
print(fullpermutation([1, 2, 3]))



if __name__ == '__main__':
    in_test()
    # split_test()
    # kk = input("jjjjjjjjj").replace("+","*").replace("-","*").replace("/","*").split("*")
    # print(kk)

    # kk = input(":\n")
    # print(kk.index("*"))
    # print(kk.find("*"))
    # print()

    aa = "abc"

    # print(aa[::-1])
    # input_multi_line()
    # input_test()
    # convert()

    a = [426, 55, 78, 2, 7, 2, 2, 7]
    b = [12, 34, 56, 4, 6]
    # print(a.count(73))
    print(b.pop())
    print(b.pop(0))
    print(b.pop(1))

    # for it in a:
    #     if it == 34:
    #         it = 100

    # print(b)
    # GetResult(b)
    # a.sort(reverse=True)
    # print(a)
    # remove_lst()
    # dict_order()
    # print(ord('A'))
    # print(ord('Z'))
    # print(ord('a'))
    # print(ord('z'))
    # print(ord('1'))
    # print(chr(100))

    # test_jiequ()
    # print(a[1:3])
    # if len(a) < 0 and 1/0 :
    #     print(a)
    # else:
    #     print(111)

    # value = int(input())
    # print_num(value)

    # reverse_str('abc')
    # reverse_str2('abc')
    # reverse_str3('abc')
    # reverse_str4('abc')
    # print(a * b)

    # k = [1, 23, 3]
    # f = [3, 23, 1]
    # z = [3, 23, 1]
    # res = set(k) == set(f)
    # res2 = k == f
    # res3 = f == z
    # print(res)
    # print(res2)
    # print(res3)
