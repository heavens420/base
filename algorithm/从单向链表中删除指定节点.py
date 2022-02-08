def delete_node():
    value = list(map(int, input().split()))

    lstr = []
    lstr.append(value[1])
    target = value[-1]
    for i in range(2, value[0] * 2 - 1, 2):
        index = lstr.index(value[i + 1])
        new_value_prefix = lstr[:index + 1]
        new_value_suffix = lstr[index + 1:]
        new_value_prefix.append(value[i])
        lstr = new_value_prefix + new_value_suffix

    ind = lstr.index(target)
    lstr.pop(ind)
    return lstr


if __name__ == '__main__':
    while 1:
        try:
            res = delete_node()
            print(" ".join(map(str, res)))
        except Exception:
            break
