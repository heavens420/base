def char_order():
    value = input()

    # 构造字典 key为字符 value为字符个数
    dd = dict()

    for i in value:
        # key不存在 即字符首次被统计 则先建立该key 防止报错 或者用defaultdict 省略此步
        if i not in dd:
            dd[i] = 0
        dd[i] += 1

    # key: 自定义排序规则 先按value排，后按key排  注意这里 value逆序 前面加了 负号
    # 排序结果返回集合，集合里面是元组
    dd = sorted(dd.items(), key=lambda x: (-x[1], x[0]), reverse=False)

    for it in range(len(dd)):
        for t in range(1):
            print(dd[it][0], end="")
    print()
    # print(f"{it}--{dd[it]}")


if __name__ == '__main__':
    while 1:
        try:
            char_order()
        except Exception:
            break
