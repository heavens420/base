def sort_word():
    words = input("输入语句：\n").split(" ")

    result1 = set()
    # 去空格和空串
    for word in words:
        if not str(word).__contains__(" ") and str(word) != '':
            result1.add(word)

    print(result1)

    result = list(result1)
    for i in range(1, len(result)):
        for j in range(len(result) - i):
            # 数字排序
            # if int(result[j]) > int(result[j + 1]):
            # 单词排序
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
            print(result)
    return result


# 35,23,5,123,54,6
if __name__ == '__main__':
    print(sort_word())
