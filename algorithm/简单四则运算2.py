import operator


def calculate(op, a, b):
    action = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }

    result = action[op](a, b)
    return result


if __name__ == '__main__':
    print(calculate('+', 10, 20))
