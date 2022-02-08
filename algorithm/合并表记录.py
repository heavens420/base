'''
[
    [],
    [],
    []
]

'''


def hebing():
    n = int(input("hang"))

    result = []
    for i in range(n):
        row = input("row").split(" ")
        result.append(row)

    lst = list()
    for k in range(len(result)):
        d = []
        sum = int(result[k][1])
        for j in range(k + 1, len(result)):
            if result[k][0] == result[j][0]:
                sum += int(result[j][1])

        d.append(result[k][0])
        d.append(sum)
        lst.append(d)

    start = None
    for it in lst:
        if it[0] == start:
            break
        start = lst[0][0]
        print(" ".join(map(str, it)))


def hebing2():
    n = int(input())
    lst = []
    dd = dict()
    for i in range(n):
        key, value = input().split()
        lst.append(int(key))
        lst.append(int(value))
        dd[key] = 0

    for it in range(0, len(lst), 2):
        dd[str(lst[it])] += int(lst[it + 1])

    for it in dd:
        print(str(it) + " " + str(dd[it]))


def hebing3():
    from collections import defaultdict

    n, dd = int(input()), dict()

    for i in range(n):
        key, value = input().split()
        # key不存在则创建 防止未创建时累加报错
        if not key in dd.keys():
            dd[key] = 0
        # key存在则直接累加
        dd[key] += int(value)

    for it in dd:
        print(str(it) + " " + str(dd[it]))





# hebing2()
hebing3()
