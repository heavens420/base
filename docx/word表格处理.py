from docx import Document

# path = r'./学生自主学习问卷调查.docx'
# path = r'C:\Users\420\Desktop\source\TimFile\TF2\学生自主学习问卷调查2－默认报告.docx'
path = r'C:\Users\420\Desktop\source\TimFile\TF2\小学思政课教学现状调查问卷－默认报告.docx'


def get_tables():
    obj = Document(path)
    tables = obj.tables
    co = 0
    for table in tables:
        co += 1
        # table = tables[t]
        for i in range(1, len(table.rows)-1):
            print(co, end="\t")
            for j in range(len(table.columns)):
                print(table.cell(i, j).text, end="\t")
            print()
        # print('-' * 30)


if __name__ == '__main__':
    get_tables()
