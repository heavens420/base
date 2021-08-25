import os

path = r'C:\Users\420\Desktop\kdgc\各省数通联系方式'

for root, dirs, files in os.walk(path):
    # for dir in dirs:
        # print(f'path = {dir}')
    for it in files:
        # print(f'word_path = r\'{os.path.join(root, it)}\'')
        print(it)

