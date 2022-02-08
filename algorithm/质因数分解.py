def judge_zhishu(num):
    if num < 2:
        return False
    if num == 2:
        return True
    for i in range(2, num // 2 + 1):
        k = num % i
        if k == 0:
            return False
    return True


def get_yinshu(num):
    result = []
    if num < 2:
        pass
    else:
        for i in range(2, num):
            k = num % i
            if k == 0:
                m = num // i
                if judge_zhishu(m):
                    result.append(m)
                else:
                    get_yinshu(m)

                if judge_zhishu(i):
                    result.append(i)
                else:
                    get_yinshu(i)
    return result


def get_num():
    num = int(input())
    for i in range(2, num // 2 + 1):
        while num % i == 0:
            num = num // i
            print(i, end=" ")


def other_test():
    a, res = int(input()), []
    for i in range(2, a // 2 + 1):
        while a % i == 0:
            a = a / i
            res.append(i)
    print(" ".join(map(str, res)) + " " if res else str(a) + " ")


if __name__ == '__main__':
    # num = int(input())
    # result = get_yinshu(num)
    # result.sort()
    # print(result)
    get_num()
    # other_test()
