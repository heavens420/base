def split_str():
    value = input()

    pre_index = 0
    for i in range(len(value) // 8):
        print(f'{value[pre_index:(i + 1) * 8]:0<8}')
        pre_index = (i + 1) * 8

    if len(value) % 8 != 0:
        print(f'{value[pre_index:]:0<8}')


if __name__ == '__main__':
    while 1:
        try:
            split_str()
        except Exception:
            break
