def get_zuobiao():
    value = input().split(";")

    start = [0, 0]
    for item in value:
        if item.strip() == '' or len(item[1:]) > 2:
            continue
        if str(item[0]).isalpha() and str(item[1:]).isdigit():
            if item[0] == 'A':
                start[0] -= int(item[1:])
            elif item[0] == 'D':
                start[0] += int(item[1:])
            elif item[0] == 'W':
                start[1] += int(item[1:])
            elif item[0] == 'S':
                start[1] -= int(item[1:])
            else:
                pass

    return start


if __name__ == '__main__':
    while 1:
        try:
            print(",".join(map(str, get_zuobiao())))
        except Exception:
            break
