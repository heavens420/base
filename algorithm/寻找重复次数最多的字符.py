def count_repeat():
    value = input()
    lst = dict()
    for i in range(len(value)):
        if value[i] not in lst.keys():
            lst[value[i]] = 1
        else:
            lst[value[i]] += 1

    # 重复最多的次数
    m = max(lst.values())

    for it in lst:
        # 找到次数最多的key
        if lst.get(it) == m:
            print(it)
