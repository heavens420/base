def get_max():
    # 体积
    w = [0, 2, 3, 4, 5]
    # 价值
    v = [0, 3, 4, 5, 6]
    # 容量
    cap = 8

    # 边界数组
    dp = [[0] * (cap + 1) for _ in range(len(w))]

    for it in dp:
        print(it)

    # i 物品编号，j 当前背包可用容量，从1开始递增 以找最优解
    for i in range(1, len(w)):
        for j in range(1, cap + 1):
            # 背包容量太小 装不下物品 则最大价值量 与 之前的价值量相同 故 i-1
            if j < w[i]:
                dp[i][j] = dp[i - 1][j]
            else:
                # 当前背包能装下编号为 i 的物品， 但是 是选择装编号i的物品还是保持之前的装载策略 要看哪种方式装的价值高
                # 如果选择装载当前编号i的物品，则要获取上一次装载的背包容量大小 即 (j - w[i]) 并在上一次装载的基础上装载本次物品 即增加价值v[i]
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - w[i]] + v[i])

    print('-' * 30)
    for it in dp:
        print(it)
    return dp[len(w) - 1][cap]


def get_max2():
    w = [2, 3, 4, 5]
    v = [3, 4, 5, 6]
    cap = 8

    dp = [[0] * (cap + 1) for _ in range(len(w) + 1)]

    for it in dp:
        print(it)

    for i in range(1, len(w) + 1):
        for j in range(cap + 1):
            if w[i - 1] > j:
                dp[i][j] = dp[i - 1][j]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - w[i - 1]] + v[i - 1])

    print('-' * 30)
    for it in dp:
        print(it)

    return dp[len(w)][cap]


if __name__ == '__main__':
    # print(get_max())
    print(get_max2())
