import re


def fake_LISP():
    ins = input("input:\n")
    expr1 = r"\("
    expr2 = r"\)"
    reg1 = re.compile(expr1)
    reg2 = re.compile(expr2)
    left = reg1.findall(ins)
    right = reg2.findall(ins)

    print(left)
    print(right)

    for i in range(len(left)):
        result = ""
        for j in range(left[len(left) - i], right[i]):
            result += ins[j]
        print(result)


def fake_LISP2():
    ins = input("input:\n")

    left = []
    right = []
    for i in range(len(ins)):
        if ins[i] == r'(':
            left.append(i)
        if ins[i] == r')':
            right.append(i)

    print(left)
    print(right)
    for i in range(len(left), 0, -1):
        result = ""
        for j in range(left[i], right[len(right) - i]):
            result += ins[j]
        print(result)


def fake_LISP3():
    ins = input("input:\n").replace(")", "").split("(")

    # for ch in ins:
    #     if ch != '':
    ins.remove('')
    return handle(ins)


def handle(content):
    # ct = str(content).strip().split(" ")
    op = ['reverse', 'quote', 'combine', 'search']
    # ct = content

    result = ''

    for ct in content:
        ct = str(ct).strip().split(" ")

        # ct[0] = str(ct[0]).strip()
        if ct[0] != '':
            if ct[0] == 'search':
                if ct[1] not in op:
                    expr = ct[2]
                    reg = re.compile(expr)
                    result = reg.search(str(ct[1])).group()

                    # index = ct[1].find(ct[2])
                    # result = ct[index]
                else:
                    handle(content)

            if ct[0] == 'combine':
                if ct[1] not in op:
                    for it in ct:
                        result += it
                        result = result.replace("combine", "")
                else:
                    handle(content)

            if ct[0] == 'quote':
                if ct[1] not in op:
                    result = ",".join(ct).replace("quote", "").replace(",", "")
                else:
                    handle(content)

            if ct[0] == 'reverse':
                if ct[1] not in op:
                    result = str(ct[1])[::-1]
                else:
                    handle(content)

    return result


if __name__ == '__main__':
    print(fake_LISP3())
