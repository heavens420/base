from docx import Document
from collections.abc import Iterator


def print_word_title():
    obj = Document('C:\\Users\\420\\Desktop\\Ca111.docx')
    # obj = [1, 2, 3]
    iterator = iter(obj.paragraphs)
    # while 1:
    #     title_level = next(iterator).style.name
    #     print(title_level)
    pre_title_level = 0
    while 1:
        try:
            title = str(next(iterator).style.name)
            if title.startswith("Heading"):
                text = str(next(iterator).text)
                level = int(title[-1:])
                print(title, end="-")
                print(text, end="-")
                print(level)
        except StopIteration:
            break


print_word_title()
