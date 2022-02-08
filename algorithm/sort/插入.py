def charu():
    lst = [12, 4, 25, 6, 17, 8, 76, 54, 32, 4]

    for i in range(len(lst)):
        pre_index = i - 1
        current = lst[i]
        while pre_index >= 0 and lst[pre_index] > current:
            lst[pre_index + 1] = lst[pre_index]
            pre_index -= 1

        lst[pre_index+1] = current

    return lst


if __name__ == '__main__':
    print(charu())
