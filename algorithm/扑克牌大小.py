'''
扑克牌游戏大家应该都比较熟悉了，一副牌由54张组成，含3~A、2各4张，小王1张，大王1张。牌面从小到大用如下字符和字符串表示（其中，小写joker表示小王，大写JOKER表示大王）：
3 4 5 6 7 8 9 10 J Q K A 2 joker JOKER
输入两手牌，两手牌之间用"-"连接，每手牌的每张牌以空格分隔，"-"两边没有空格，如：4 4 4 4-joker JOKER。
请比较两手牌大小，输出较大的牌，如果不存在比较关系则输出ERROR。
基本规则：
（1）输入每手牌可能是个子、对子、顺子（连续5张）、三个、炸弹（四个）和对王中的一种，不存在其他情况，由输入保证两手牌都是合法的，顺子已经从小到大排列；
（2）除了炸弹和对王可以和所有牌比较之外，其他类型的牌只能跟相同类型的存在比较关系（如，对子跟对子比较，三个跟三个比较），不考虑拆牌情况（如：将对子拆分成个子）；
（3）大小规则跟大家平时了解的常见规则相同，个子、对子、三个比较牌面大小；顺子比较最小牌大小；炸弹大于前面所有的牌，炸弹之间比较牌面大小；对王是最大的牌；

（4）输入的两手牌不会出现相等的情况。

数据范围：字符串长度：

输入描述：
输入两手牌，两手牌之间用"-"连接，每手牌的每张牌以空格分隔，"-"两边没有空格，如 4 4 4 4-joker JOKER。

输出描述：
输出两手牌中较大的那手，不含连接符，扑克牌顺序不变，仍以空格隔开；如果不存在比较关系则输出ERROR。
'''


def get_max():
    value = input().split("-")

    # 单张与单张比较
    # if len(value[0]) == len(value[1]) and len(value[0]) == 1:
    #     return max(value[0][0], value[1][0])
    #
    # # 对子与对子比较
    # elif len(value[0]) == len(value[1]) and len(value[0]) == 2:
    #     return max(value[0][0], value[1][0])
    #
    # # 三张与三张比较
    # elif len(value[0]) == len(value[1]) and len(value[0]) == 3:
    #     return max(value[0][0], value[1][0])
    #
    # # 顺子与顺子比较
    # elif len(value[0]) == len(value[1]) and len(value[0]) == 5:
    #     return max(value[0][0], value[1][0])

    # 炸弹不含王炸与炸弹比较
    v1 = value[0].split()
    v2 = value[1].split()

    for i in range(len(v2)):
        if v2[i] == 'J':
            v2[i] = '11'
        elif v2[i] == 'Q':
            v2[i] = '12'
        elif v2[i] == 'K':
            v2[i] = '13'
        elif v2[i] == 'A':
            v2[i] = '14'
        elif v2[i] == '2':
            v2[i] = '15'
        elif v2[i] == 'JOKER':
            v2[i] = '17'
        elif v2[i] == 'joker':
            v2[i] = '16'

    for i in range(len(v1)):
        if v1[i] == 'J':
            v1[i] = '11'
        elif v1[i] == 'Q':
            v1[i] = '12'
        elif v1[i] == 'K':
            v1[i] = '13'
        elif v1[i] == 'A':
            v1[i] = '14'
        elif v1[i] == '2':
            v1[i] = '15'
        elif v1[i] == 'JOKER':
            v1[i] = '17'
        elif v1[i] == 'joker':
            v1[i] = '16'

    # 王炸与其它比较
    wz = ['16', '17']
    if set(wz) - set(v1)== set():
        return value[0]
    elif set(wz) - set(v2) == set():
        return value[1]
    # 其它相同类型比较
    elif len(v1) == len(v2):
        res = max(int(v1[-1]), int(v2[-1]))
        result = value[0] if res == int(v1[-1]) else value[1]
        return result
    # 炸与其它比较
    elif len(v1) == 4 and len(v2) != 4:
        return value[0]
    elif len(v2) == 4 and len(v1) != 4:
        return value[1]
    # 无法比较
    else:
        return 'ERROR'


if __name__ == '__main__':
    while 1:
        try:
            res = get_max()
            print(res)
        except Exception:
            break
