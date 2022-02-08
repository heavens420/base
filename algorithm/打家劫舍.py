def get_max():
    value = list(map(int, input().split()))

    dp = [0 for _ in range(len(value))]
    if len(value) > 1:
        dp[0] = value[0]
        dp[1] = max(value[0], value[1])
    else:
        print('输入非法')
        return 

    for i in range(2, len(value)):
        # 对于当前这一间 无非两种情况 抢或者不抢 只要比较这两种情况的最优解即可
        # 　dp[i-1] : 不抢这一间  dp[i-2]：抢这一间，则要先得到前前一间的最优解加上这一间，
        dp[i] = max(dp[i - 1], dp[i - 2] + value[i])

    return dp[len(value) - 1]


if __name__ == '__main__':
    while 1:
        print(get_max())
