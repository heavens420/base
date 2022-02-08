'''

地上有一个m行n列的方格，从坐标 [0,0] 到坐标 [m-1,n-1] 。一个机器人从坐标 [0, 0] 的格子开始移动，它每次可以向左、右、上、下移动一格（不能移动到方格外），
也不能进入行坐标和列坐标的数位之和大于k的格子。例如，当k为18时，机器人能够进入方格 [35, 37] ，因为3+5+3+7=18。但它不能进入方格 [35, 38]，因为3+5+3+8=19。
请问该机器人能够到达多少个格子？

输入：m = 2, n = 3, k = 1
输出：3

输入：m = 3, n = 1, k = 0
输出：1


来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/ji-qi-ren-de-yun-dong-fan-wei-lcof
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
'''


def walk():
    m, n, k = eval(input())

    count_list = []
    for t in range(m):
        for i in range(n):
            res = get_num(str(t)) + get_num(str(i))
            if res <= k:
                count_list.append(res)
    return len(count_list)


def get_num(num):
    sum = 0
    for i in range(len(num)):
        sum += int(num[i])
    return sum


if __name__ == '__main__':
    count = walk()
    print(count)
