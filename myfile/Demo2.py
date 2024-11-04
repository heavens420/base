import os


def changeFileNames(path: str):
    for root, dirs, files in os.walk(path):
        print(f'root======文件路径，即入参path========{root}')
        print(f'dirs======文件路径下的文件夹列表========={dirs}')
        print(f'files=====文件夹下的文件列表=============={files}')
        i = 0
        for file in files:
            i += 1
            newFileName = f"{i}-{file}"
            fullPathFileName = os.path.join(root, file)
            newFileNameFullPath = os.path.join(root, newFileName)
            # print(fullPathFileName)
            os.rename(fullPathFileName, newFileNameFullPath)
            # break
        break

def mystery_function(x):
    result = []
    for i in range(x):
        result.append(i)
        if i % 2 == 0:
            result.pop()
    return result


if __name__ == '__main__':
    # path = r'C:\Users\heave\Desktop\npmDepency'
    # changeFileNames(path)
    output = mystery_function(5)
    print(output)
