from docx import Document

# path = r'C:\Users\420\Desktop\IPC接口测试\IP测试记录汇总20210715.docx'
path = r'C:\Users\420\Desktop\IDC数通设备调研表-安徽.docx'
obj = Document(path)

for content in obj.paragraphs:
    title = content.style.name
    if str(title).startswith("Heading 3"):
        print(content.text)
