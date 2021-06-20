from docx import Document
import re

max_level1 = 0
level1 = 0
obj = Document('C:\\Users\\420\\Desktop\\Ca111.docx')
key = 0
dic = {}
for content in obj.paragraphs:
    if re.match("^Heading \d+$", content.style.name):
        level1 = int(content.style.name[-1:])
        if max_level1 < level1:
            max_level1 = level1
    if content.style.name == 'Heading 1':
        print(max_level1)
        dic[key] = max_level1
        key = key + 1
