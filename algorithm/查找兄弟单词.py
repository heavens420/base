
def get_words():
    value = input().split()

    res = []
    for i in range(1, len(value) - 2):
        s = []
        for k in value[i]:
            s.append(k)
        res.append(s)

    target = []
    for k in value[-2]:
        target.append(k)

    result = []
    for item in res:
        if not item == target and is_same(item, target):
            result.append(item)

    result.sort()
    # return result
    if len(result) >= int(value[-1]):
        return "".join(map(str, result[int(value[-1]) - 1])), len(result)
    else:
        return '', len(result)


# 元素是否相同判断函数
def is_same(list1, list2):
    if sorted(list2) == sorted(list1):
        return True
    else:
        return False


if __name__ == '__main__':
    while 1:
        try:
            res, n = get_words()
            print(n)
            if res != '':
                print(res)
        except Exception as e:
            # print(e)
            break
