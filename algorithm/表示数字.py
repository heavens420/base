def ex_num():
    value = list(input())
    # 加个空串  用于判断最后一位是数字的情况 补 *
    value.append('')

    lstr = ''
    pre_char = ''
    for item in value:
        # 前一位不是数字 当前位是数字 当前位前面加 *
        if str(item).isdigit() and not pre_char.isdigit():
            lstr += '*' + item
        # 前一位是数字 当前位不是数字 当前位前面加 *  如果数字是最后一位 则后面无元素 也就无法 在数字后面加 *  故 列表提前加了空串
        elif pre_char.isdigit() and not str(item).isdigit():
            lstr += '*' + item
        else:
            lstr += item
        pre_char = item

    return lstr


if __name__ == '__main__':
    while 1:
        try:
            print(ex_num())
        except Exception:
            break
