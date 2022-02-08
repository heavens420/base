'''
    第1，n两间相连 即只能打劫1，2，3...2*(n-1)间或者 2,3,4...2*n间  最终比较两种策略的最优解

'''


def get_max():
    value = list(map(int, input().split()))

    # 1 ~ (n-1) 间dp数组
    dp = [0 for _ in range(len(value))]
    # 2 ~ n 间dp数组
    dp2 = [0 for _ in range(len(value))]
    if len(value) <= 0:
        print('输入非法')
        return

    if len(value) <= 2:
        return max(value)

    if len(value) > 2:
        dp[0] = value[0]
        dp2[1] = value[1]
        dp[1] = max(value[0], value[1])
        dp2[2] = max(value[2], value[1])
    else:
        print('输入非法')

    for i in range(2, len(value) - 1):
        dp[i] = max(dp[i - 1], dp[i - 2] + value[i])

    for j in range(3, len(value)):
        dp2[j] = max(dp2[j - 1], dp2[j - 2] + value[j])

    return max(dp[-2], dp2[-1])
    # return dp,dp2


if __name__ == '__main__':
    while 1:
        print(get_max())
