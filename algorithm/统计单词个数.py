import re


def count_num():
    words = input("输入语句：\n").split(" ")

    result = set()
    for i in range(len(words)):
        reg = re.compile(words[i])
        singe_word = reg.findall(str(words))
        result.add(tuple(singe_word))

    for item in result:
        print(f"{item[0]}:{len(item)}")


def count_num2():
    result = set()
    words = input("输入语句：\n").split(" ")
    for i in range(len(words)):
        single_word = []
        for j in range(len(words)):
            if words[i] == words[j]:
                single_word.append(words[i])
        result.add(tuple(single_word))
        # single_word.clear()

    for item in result:
        print(f"{item[0]}:{len(item)}")


if __name__ == '__main__':
    # count_num()
    print("-" * 30)
    count_num2()
