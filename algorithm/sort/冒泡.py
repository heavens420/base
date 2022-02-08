def maopao():
    lst = [1, 2, 54, 5563, 2343, 434, 2, 34, 234, 24, 23]

    for i in range(1, len(lst)):
        for j in range(len(lst) - i):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j],
            print(lst)
    return lst


if __name__ == '__main__':
    print(maopao())
