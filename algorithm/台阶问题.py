'''
一个楼梯有n个台阶，每一步可以走一个台阶，也可以走两个台阶，请问走完这个楼梯共有多少种方法？


很简单的一道题，学过组合数学的人很快就能想到，这是一个递推关系。假设走完k个台阶有f(k)种走法。

k = 1时，f(k) = 1
k = 2时，f(k) = 2
k = n时，第一步走一个台阶，剩n-1个台阶，有f(n - 1)种走法。第一步走两个台阶，剩n-2个台阶，有f(n - 2)种走法。所以共有f(n - 1) + f(n - 2)种走法。

'''


#  递归 时间复杂度 O(2^n)
def get_num(n):
    if n == 1:
        return 1
    elif n == 2:
        return 2
    else:
        return get_num(n - 1) + get_num(n - 2)


# 备忘录方式 记录已经计算过的f(n)避免重复计算 时间复杂度O(n)
def get_num2(n, di):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    if n == 2:
        return 2
    if n in di.keys():
        return di.get(n)
    else:
        num = get_num2(n - 1, di) + get_num2(n - 2, di)
        di[n] = num
        return num


# 动态规划 时间复杂度 O(n) 空间复杂度O(1)
def get_num3(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    if n == 2:
        return 2

    # 相当于f(n-2)
    a = 1
    # 相当于f(n-1)
    b = 2
    # temp 相当于f(n)
    temp = 0

    for i in range(3, n + 1):
        temp = a + b
        #
        a, b = b, temp

    return temp


if __name__ == '__main__':
    while 1:
        try:
            di = dict()
            n = int(input())
            # print(get_num(n))
            # print(get_num2(n, di))
            print(get_num3(n))
        except Exception:
            break
