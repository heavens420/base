import os


# res = os.popen("rm -fr ./111.txt")

# res = os.system("ls -l ../*")
# res = os.system("rm -fr ./111.txt")
# print(res)


def aa():
    a = 1 / 0


if __name__ == '__main__':
    while 1:
        try:
            aa()
        except Exception as e:
            print(e)
        print(111111)
