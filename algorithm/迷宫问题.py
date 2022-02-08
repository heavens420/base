

'''

0 1 0 0 0
0 1 1 1 0
0 0 0 0 0
0 1 1 1 0
0 0 0 1 0

'''


def migong(mig, m, n):
    for k in range(m - 1):
        for h in range(n - 1):
            if mig[k + 1][h + 1] == 0 and k + 1 == m - 1 and h + 1 == n - 1:
                print(f"{k + 1} {h + 1}")
            # 向右走
            elif h + 1 < n and mig[k][h] == mig[k][h + 1]:
                print(f"{k + 1} {h + 1}")
                migong(mig, k, h)
            # 向下走
            elif k + 1 < m and mig[k][h] == mig[k + 1][h]:
                print(f"{k + 1} {h + 1}")
                migong(mig, k, h)
            # 向左走
            elif h - 1 >= 0 and mig[k][h] == mig[k][h - 1]:
                print(f"{k + 1} {h + 1}")
                migong(mig, k, h)
            # 向上走
            elif k - 1 >= 0 and mig[k][h] == mig[k - 1][h]:
                print(f"{k + 1} {h + 1}")
                migong(mig, k, h)
            else:
                print('死路')


if __name__ == '__main__':
    m, n = map(int, input().split())

    # mig = [[0 for j in range(n)] for i in range(m)]
    mig = []

    for i in range(m):
        col = list(map(int, input().split()))
        mig.append(col)

    print("0 0")
    migong(mig, m, n)
