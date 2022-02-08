def yasuo():
    value = input()
    lst = dict()
    for i in range(len(value)):
        if value[i] not in lst.keys():
            lst[value[i]] = 1
        else:
            lst[value[i]] += 1

    lstr = ""
    for it in lst:
        if lst[it] > 1:
            lstr += str(lst.get(it)) + str(it)
        else:
            lstr += str(it)
    print(lstr)


if __name__ == '__main__':
    while 1:
        yasuo()
