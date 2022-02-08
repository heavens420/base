import random
import os

for i in range(10):
    a = random.uniform(0.01, 0.5)
    # print(a)

    img_file = "./排序算法.jpg"
    # print(img_file.split("."))


def ddd():
    A = input("输入字符串1：")
    B = input("输入字符串2：")

    def minDistance(w1, w2):
        m, n = len(w1), len(w2)
        if (m == 0):
            return m
        if (n == 0):
            return n
        # 构造全0二维数组用于保存每次比较结果
        step = [[0] * (n + 1) for _ in range(m + 1)]
        # 二维数组边界赋值，用于记录比较次数
        for i in range(1, m + 1): step[i][0] = i
        for j in range(1, n + 1): step[0][j] = j
        # 遍历二维数组 逐一比较两个字符串的每一个值是否相同
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # 如果字符串中存在相同的字符 不同的数量置为0 否则置为1
                if w1[i - 1] == w2[j - 1]:
                    diff = 0
                else:
                    diff = 1
                '''构造dp条件：用二维数组保存每次比较的结果，在边界矩阵的基础上，每一个新的值都是根据上一步计算出来的最小值，最小值即为要改变的最小次数，比如对于如下矩阵
                    [0, 1, 2, 3]
                    [1, 1, 2, 3]
                    [2, 2, 2, 3]
                    [3, 0, 0, 0]
                    step[1][1]的值是[0, 1, 2, 3]和最左边一列逐一比较的最小值(复制不了)加上w1[0][0]和w2[0][0]的比较结果(记为a)再和比较[0][0]决定(记为b)，b和a比较的原因是，假设当前字符相同，
                    则需要变换的次数就是0，而a的值为1 故b和a的最小值才是当前需要编辑次数的最小值，如果输入的两个字符串都是一个字符那么比较到此结束，如果两字符相同则step[1][1]的值为0，因为diff=0，加上step[0][0]
                    如果两字符串不同则diff=1，加上[0][0]=0,step[1][1]=1 故结果为1。以此类推，step[i][j]用于都是当前问题的子问题的最优解，当所有子问题解决完毕，最后的step[i][j]即为该问题的最优解
                '''
                step[i][j] = min(step[i - 1][j - 1], min(step[i - 1][j], step[i][j - 1])) + diff
            for it in step:
                print(it)
            print('---------------------------------')
        return step[m][n]

    print(minDistance(A, B))


ddd()

# def test_while():
#     i = 0
#     while 1:
#         print(1)
#         i += 1
#         s = i / 0
#         if i == 10:
#             return i


# test_while()
#
#
# def test_not():
#     aqq = 4 > 1
#     if not aqq:
#         print(111)
#     else:
#         print(222)
#
#
# def test_os_size():
#     cmd = "wc -c ."
#     size = os.popen(cmd)
#     print(size.read())
#
#
# def test_size2():
#     size = os.path.getsize("../database/demo1.py")
#     print(size)



# if __name__ == '__main__':
    # test_not()
    # test_os_size()
    # test_size2()
