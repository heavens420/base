'''
    先确定一个对子 其它的只要全部满足 abc或者zzz形式 即为胡牌

'''


#  不对
def hupai():
    value = input()

    value = list(value)
    value.sort()

    for i in value:
        if len(value) == 2:
            if value[0] == value[1]:
                return 'yes'
        #
        # elif len(value) == 5:
        #     # xxx yy  形式
        #     if value[0] == value[2]:
        #         if value[1] == value[0] and value[3] == value[4]:
        #             return 'yes'
        #     elif value[0] == value[1]:  # pp ttt 形式
        #         if value[2] == value[3] and value[3] == value[4]:
        #             return 'yes'
        #     else:
        #         return 'no'

        elif len(value) == 5 or len(value) == 8 or len(value) == 11 or len(value) == 14:
            dui, shun, ke = get_pai_type(value)
            if dui == 1 and shun + ke >= 1:
                return 'yes'
            else:
                return 'no'
        else:
            return 'no'


# 获取牌的类型
def get_pai_type(num):
    # 最大相同次数
    count = 1
    # 最大连续次数
    lianxu = 1

    # 对子个数
    dui = 0
    # 顺子个数
    shun = 0
    # 刻子个数
    kezi = 0

    for i in range(1, len(num)):
        if num[i] == num[i - 1]:
            count += 1
        if int(num[i]) - 1 == int(num[i - 1]):
            lianxu += 1

        # 有俩一样的就认为有一个对子
        if count == 2:
            dui += 1
        # 有仨一样的就认为有一个刻子，有可能有杠，但是刻子就不是对子 故对子要减 1
        if count >= 3:
            kezi += 1
            dui -= 1
        # 有仨连续的就认为有一个顺子 有可能有杠
        if lianxu >= 3:
            shun += 1

        if count == 4:
            dui -= 2

    return dui, shun, kezi


# -------------------------------------------------------


def find_duizi(arr):
    dui_lst = []
    pre_index = 0
    for i in range(len(arr) - 1):
        if arr[i] == arr[i + 1] and pre_index + 1 != i:
            # 把对子所在索引返回
            dui_lst.append(i)
            pre_index = i

    return dui_lst


def find_kezi(arr):
    kezi_lst = []
    pre_index = 0
    for i in range(2, len(arr)):
        if arr[i] == arr[i - 1] and arr[i] == arr[i - 2] and pre_index + 1 != i:
            kezi_lst.append(i)
            pre_index = i
    return kezi_lst


def find_shunzi(arr):
    shunzi_lst = []
    for i in range(2, len(arr)):
        if int(arr[i]) == int(arr[i - 1]) + 1 and int(arr[i]) == int(arr[i - 2]) + 2:
            shunzi_lst.append(i)
    return shunzi_lst


def judge_hu(value):
    duizi_lst = find_duizi(value)
    if len(duizi_lst) == 0:
        return 'no'

    remove_lst = []
    # 先把对子确定 然后去掉 从里面找顺子和刻子
    for i in duizi_lst:
        # 先保存要移除的对子 如果有多个对子 则要把之前移除错误的加回来
        remove_lst.append(value[i])
        remove_lst.append(value[i+1])
        # 先删除大的索引 后删除小的索引 否则索引发生变化 导致删错
        value.remove(value[i + 1])
        value.remove(value[i])

            # 只有一个对子牌(对子已经在上面移除了所以是0) 直接胡
        if len(value) == 0:
            return 'yes'

        kezi_lst = find_kezi(value)

        kezi = len(kezi_lst)
        # 去除对子后的牌 张数
        pai_len = len(value)

        # 如果剩下的牌 都是刻子 则直接胡牌
        if kezi * 3 == pai_len:
            return 'yes'

            # 剩下的全是顺子
        if kezi == 0:
            shunzi_lst = find_shunzi(value)
            # 如果全是顺子 胡牌
            if len(shunzi_lst) * 3 == pai_len:
                return 'yes'
            # else:
            #     return 'no'
        # 不全是顺子  有顺子 有刻子
        else:
            # 把刻子都去了 方便找顺子
            # 先删大索引后删小索引 防止索引变动 删除异常
            kezi_lst.reverse()
            for k in kezi_lst:
                remove_lst.append(value[k])
                remove_lst.append(value[k-1])
                remove_lst.append(value[k-2])
                value.remove(value[k])
                value.remove(value[k - 1])
                value.remove(value[k - 2])

            shunzi_lst = find_shunzi(value)

            # 除去对子 剩下的都是刻子和顺子
            if len(shunzi_lst) * 3 + kezi * 3 == pai_len:
                return 'yes'
        value += remove_lst
        remove_lst = []
        value.sort()
    return 'no'


if __name__ == '__main__':
    while 1:
        value = input()

        value = list(value)
        value.sort()

        # print(hupai())
        print(judge_hu(value))
