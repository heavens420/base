def xuanze():
    lst = [23, 4, 5, 43, 45, 654, 5, 6, 542, 3, 2, 3]

    for i in range(len(lst)):
        # 记录最小值
        min = lst[i]
        # 记录最小值对应索引
        min_index = i
        for j in range(i + 1, len(lst)):
            if min > lst[j]:
                min = lst[j]
                min_index = j
        # 交换最小值和当前值位置
        lst[min_index], lst[i] = lst[i], min

    return lst


if __name__ == '__main__':
    print(xuanze())
