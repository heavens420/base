def getMinStep():
    dp = [[0] * len(b) for _ in range(len(a))]

    for i in range(len(b)):
        dp[0][i] = i
    for j in range(len(a)):
        dp[j][0] = j
    printArray(dp)
    print('----123------------', end='\n')
    for i in range(len(a)):
        for j in range(len(b)):
            if a[i] == b[j]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1]) + 1
            printArray(dp)
            print('------------', end='\n')
    return dp[len(a) - 1][len(b) - 1]


def printArray(dp):
    for i in range(len(a)):
        print(dp[i])


'''
俩字符串 新增删除修改任一字符串 使俩字符串相同 求最小操作次数
'''

if __name__ == '__main__':
    a = "sefsq"
    b = "ddaq"
    print(getMinStep())
