import random
import time

'''
掷骰子游戏：每个骰子有6面，点数分别为1，2，3，4，5，6.游戏者在程序开始时输入一个无符号整数，作为产生随机数的种子。每轮掷两次骰子，第一轮如果和数为7或11则为胜，游戏结束；和数为2，3或12则为负，游戏结束；和数为其他值，则将此值作为自己的点数，继续第二轮，第三轮。。。直到某轮的和数等于点数则取胜，若在此前出现和数为7则为负。

'''

def zhi():
    shaizi = [1, 2, 3, 4, 5, 6]

    num1 = random.choice(shaizi)
    num2 = random.choice(shaizi)

    total = num2 + num1

    # print(f"第1轮总和:{total}")
    if total == 7 or total == 11:
        # print('win1')
        return 'win'

    elif total == 2 or total == 3 or total == 12:
        # print('lose2')
        return 'lose'

    else:
        sum = 0
        count = 2
        while total != sum:
            num2 = random.choice(shaizi)
            num1 = random.choice(shaizi)

            sum = num2 + num1
            # print(f"第{count}轮总和：{sum}")
            count += 1

            if sum == 7:
                # print('lose3')
                return 'lose'

        if total == sum:
            # print('win4')
            return 'win'


if __name__ == '__main__':
    n = 100000000
    m = n
    num = 0
    while n:
        n -= 1
        res = zhi()
        if res == 'win':
            num += 1
        # print('-' * 30)
        # time.sleep(1)
    print(num/m)