def pai_lie():
    n = int(input())
    for i in range(n):
        start = int(input())
        if 4 > start >= -9:
            show_line(start)
        else:
            # raise Exception("Out of heap space")
            print("Out of heap space")

def show_line(start):
    num_list = []
    for i in range(0, 6):
        num_list.append(start + i)
    sort_line(num_list)


def sort_line(num_list):
    print(f"{num_list[-1]} {num_list[-2]} {num_list[-3]}")
    print(f"{num_list[2]} {num_list[1]} {num_list[0]}")

    print(f"{num_list[-1]} {num_list[-3]} {num_list[-4]}")
    print(f"{num_list[-2]} {num_list[-5]} {num_list[-6]}")

    print(f"{num_list[-1]} {num_list[-2]} {num_list[-5]}")
    print(f"{num_list[-3]} {num_list[-4]} {num_list[-6]}")

    print(f"{num_list[-1]} {num_list[-3]} {num_list[-5]}")
    print(f"{num_list[-2]} {num_list[-4]} {num_list[-6]}")

    print(f"{num_list[-1]} {num_list[-2]} {num_list[-4]}")
    print(f"{num_list[-3]} {num_list[-5]} {num_list[-6]}")


if __name__ == '__main__':
    pai_lie()
