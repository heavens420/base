def collect_fu():
    lst = input().split(",")
    count = []
    for i in range(5):
        value = 0
        for k in range(len(lst)):
            value += int(lst[k][i])

        count.append(value)

    count.sort()
    print(count)
    print(count[0])
    print(min(count))


while 1:
    collect_fu()
