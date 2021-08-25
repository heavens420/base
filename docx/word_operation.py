from docx import Document
import re


def get_max_level():
    obj = Document('C:\\Users\\420\\Desktop\\Ca111.docx')
    max_level1 = 0
    key = 0
    dic = {}
    for content in obj.paragraphs:
        if re.match("^Heading \d+$", content.style.name):
            level1 = int(content.style.name[-1:])
            if max_level1 < level1:
                max_level1 = level1
        # if content.style.name == 'Heading 1':
            # print(max_level1)
            dic[key] = max_level1
            max_level1 = 0
            key = key + 1
    print(dic)
    return dic


def print_word_title():
    obj = Document('C:\\Users\\420\\Desktop\\Ca111.docx')
    back_level = 0
    dic = get_max_level()
    max_level = 0
    key = 1
    for content in obj.paragraphs:
        # if content.style.name == 'Heading 1':
        # if content.text == '总体功能要求':
        if re.match("^Heading \d+$", content.style.name):
            level = int(content.style.name[-1:])
            # if level == 1:
            #     key = key + 1
            max_level = dic.get(key)
            if level - back_level == 1:
                if level == max_level:
                    print(content.text)
                    back_level = 0
                    key = key + 1
                else:
                    print(content.text, end="-")
                    back_level = level
            else:
                for i in range(level - 1):
                    print("-", end="")
                if level == max_level:
                    print(content.text)
                    back_level = 0
                    # key = key + 1
                else:
                    print(content.text, end="")
                    back_level = 0
                    # key = key + 1


print_word_title()
