def get_max():
    value = list(map(int, input().split()))

    sum = 0
    dp = [0 for i in range(len(value))]

    for i in range(0, len(value)):
        if value[i] < 0:
            dp[i] = max(dp[i - 1], sum)
            sum = 0
        else:
            sum += value[i]
            dp[i] = sum
    return dp


if __name__ == '__main__':
    while 1:
        print(get_max())
