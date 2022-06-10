import os
import re


path = r'C:\Users\420\Documents\WeChat Files\wxid_d6s6ieyj6kyd12\FileStorage\File\2022-02\搞笑'


def batch_change_file_name():
    for root, dirs, files in os.walk(path):
        for file in files:
            # print(file, end="\n")
            new_file_name = str(file).replace("搞笑", "").replace("-1", "").replace("-2", "")
            os.chdir(path)
            if not os.path.exists(new_file_name):
                os.rename(str(file), new_file_name)


if __name__ == '__main__':
    batch_change_file_name()
