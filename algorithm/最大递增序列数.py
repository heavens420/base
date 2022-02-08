def asc_most():
    n = int(input())
    value = list(map(int, input().split()))

    lst = []
    for i in range(1, n):
        cou = 1
        k = i
        temp = value[k - 1]
        while k != n - 1:
            if value[k] > temp:
                temp = value[k]
                cou += 1
            k += 1

            # else:
            #     break

        lst.append(cou)

    return lst


# 动态规划
def asc_most2():
    n = int(input())

    value = list(map(int, input().split()))

    dp = [1 for i in range(len(value))]

    print(dp)
    for i in range(len(value)):
        for j in range(i):
            if value[i] > value[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


if __name__ == '__main__':
    while 1:
        try:
            # res = asc_most()
            res = asc_most2()
            print(res)
        except Exception:
            break
