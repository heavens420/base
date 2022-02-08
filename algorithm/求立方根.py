def m3():
    value = float(input())
    print(pow(value, 1 / 3))
    # k = 1
    # while 1:
    #     if k * k * k == value:
    #         return k
    #     k += 1
    #
    #     if k >= value // 2:
    #         break

    t = 1.0
    while 1:
        if t * t * t - value > 0.01:
            t = t - 0.01
        elif t * t * t - value < -0.01:
            t = t * 1.1
        else:
            return t


if __name__ == '__main__':
    while 1:
        try:
            print(f'{m3():.1f}')
        except Exception:
            break
