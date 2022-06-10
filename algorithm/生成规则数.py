import random


def calculate(sum, n):
    mid = sum // n
    nums = [mid for i in range(n)]
    total = get_sum(nums)

    # 计算每个元素要加的数量
    cha = sum - total
    avg = cha // n
    # 如果平均每个元素要增加的数量为0 即只能部分元素增加
    if avg == 0:
        nums[0] += cha
        print(nums)

    print("-" * 30)

    for i in range(n // 2):
        ran = random.randint(total // (10 * n), total // (3 * n))
        nums[i] -= ran
        nums[n - i - 1] += ran

    print(nums)


def get_sum(array) -> int:
    total = 0
    for it in array:
        total += it
    return total


def get_score_per_option(score, man):
    mid_score = score // 3 * 2
    # 假设各有1/3人数分别选择了2分和3分的选项
    s2 = mid_score // 2
    s3 = mid_score // 2
    # 各有1/6的人数分别选择了0分和4分选项

    # 把人数分成13-30份
    ran = random.randint(13, 30)
    per = 574 / ran

    # 5个选项对应人数大致为 x 2x 4x 4x

    sc = [0 for i in range(5)]

    # 0分 7-100人
    sc[0] = random.randint(7, 100)
    sc[1] = random.randint(25, 200)
    sc[2] = random.randint(80, 300)
    sc[3] = random.randint(80, 300)
    sc[4] = random.randint(7, 100)

    sum_man = get_sum(sc)
    if sum_man < man:
        cha = man - sum_man
        mid_cha = cha // 2
        sc[2] += mid_cha
        sc[3] += cha - mid_cha
    elif sum_man > man:
        cha = sum_man - man
        mid_cha = cha // 2
        mx = max(sc[0], sc[4])
        mn = min(sc[0],sc[4])
        if mx - mid_cha > man * 0.25:
            mx -= mid_cha
            if mn - mid_cha > man * 0.25:
                mn -= mid_cha
            else:



if __name__ == '__main__':
    calculate(6989, 5)
