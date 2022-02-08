'''
    给定不同面值的零钱和总数 要求用最少张数的零钱拼凑出总数

    转化成背包问题：总数视为背包容量，零钱视为物品列表，每个物品两个选择，拿或者不拿
    dp[i] 为最少硬币个数
    dp[i] = min(dp[i],dp[i-coin]+1) i：背包容量
    dp[i]代表当前物品不拿  dp[i-coin]+1 代表拿 所以零钱数量加1
    不和dp[i-1]比较的原因是 前一个未必是最优解 因为total不一样 拆分策略不一样 结果不一样
'''


def get_min():
    total = int(input())
    coins = list(map(int, input().split()))

    dp = [total for _ in range(total + 1)]
    dp[0] = 0
    for i in range(1, total + 1):
        for j in range(len(coins)):
            if coins[j] <= i:
                dp[i] = min(dp[i], dp[i - coins[j]] + 1)
    return dp


if __name__ == '__main__':
    while 1:
        print(get_min())
