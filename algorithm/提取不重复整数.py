def get_zs():
    num = input()
    lst = []
    dd = dict()
    num = list(num)
    num.reverse()
    for i in num:
        if i not in dd.keys():
            lst.append(i)
        dd[str(i)] = 0

    for it in lst:
        print(it, end="")


get_zs()
