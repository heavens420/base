import sys

if __name__ == '__main__':
    a1 = input('请输入教师人员excel文件全路径：')
    a2 = input('请输入课程表excel文件全路径：')

    print(a1)
    print(a2)
    with open(a1,'r',encoding='utf-8') as file:
        content = file.read()
        print(content)