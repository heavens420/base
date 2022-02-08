'''
    1 2
    2 3

    4 5 7
    3 4 6

    3 4
    4 5
    6 7


    1
    2

    3
    4
    5
'''


def chengfa():
    row1 = int(input())
    col_row = int(input())
    col = int(input())

    ju1 = []
    ju2 = []
    for i in range(row1):
        row_lst = list(map(int, input().split()))
        ju1.append(row_lst)

    for j in range(col_row):
        row_lst2 = list(map(int, input().split()))
        ju2.append(row_lst2)

    ju2 = reverse_juzhen(ju2)
    result = [[0 for j in range(col)] for i in range(row1)]

    for k in range(len(ju1)):
        for u in range(len(ju2)):
            for v in range(col_row):
                result[k][u] += ju1[k][v] * ju2[u][v]

    return result


def reverse_juzhen(lst):
    if len(lst) == 0:
        return [[]]
    row_num = len(lst)
    col_num = len(lst[0])

    target = [[0 for j in range(row_num)] for i in range(col_num)]

    for i in range(len(lst)):
        for j in range(len(lst[i])):
            target[j][i] = lst[i][j]

    return target


if __name__ == '__main__':
    # lst = [
    #     [1, 2, 3],
    #     [4, 5, 6]
    # ]
    # res = reverse_juzhen(lst)
    # for it in res:
    #     print(it)
    while 1:
        try:
            res = chengfa()
            for it in res:
                print(" ".join(map(str,it)))
        except Exception:
            break
