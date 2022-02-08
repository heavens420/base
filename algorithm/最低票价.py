'''
    天：[1,4,6,7,8,20]   1 4 6 7 8 20
    价：[2,7,30] 对应天，周月票

    四种可能：不买票(当天不是旅行日)，买日票，周票，月票，对应的价格最小即可，其中买周票需要获取一周前价格最优解，月票同理
            不买票则当前花费和前一天相同，不参与比较 否则最终结果都是不买票的累计
    最低价：dp[i] = min(dp[i-1]+prices[0],dp[i-7]+prices[1],dp[i-30]+prices[2])
'''


def get_min():
    # 票价
    prices = list(map(int, input().split()))
    # 　旅行的天
    days = list(map(int, input().split()))

    dp = [0 * max(prices) for _ in range(365 + 31)]
    index = 0
    for i in range(31, 396):

        # 旅行天数遍历结束
        if len(days) - 1 < index:
            break
        # 今天不旅行 即旅行数组对应天数不存在
        if days[index] != i - 30:
            dp[i] = dp[i - 1]
        else:  # 今天旅行
            dp[i] = min(dp[i - 1] + prices[0], dp[i - 7] + prices[1], dp[i - 30] + prices[2])

            # 当前天数旅行完成 才能进行下一天旅行
            index += 1

    return dp[max(days) + 30]


if __name__ == '__main__':
    while 1:
        print(get_min())
