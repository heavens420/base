import json
from mydocx import Document
import re

# doc_path = r'C:\Users\420\Desktop\kdgc\6月集团考核\IPC接口测试\IP测试记录汇总20210715.mydocx'
# doc_path = r'C:\Users\420\Desktop\王涛IP测试记录.mydocx'
# doc_path = r'C:\Users\420\Desktop\IP测试-李亚辉.mydocx'
doc_path = r'C:\Users\420\Desktop\IP指令附加测试0825.mydocx'
# json_path = r'C:\Users\420\Desktop\IP中期考核.json'
# json_path = r'C:\Users\420\Desktop\IP中期考核-王涛.json'
# json_path = r'C:\Users\420\Desktop\0707已测试IP.postman_collection.json'
json_path = r'C:\Users\420\Desktop\IP中期附加.json'


def get_my_api_name():
    api_list = list()
    # count = 0
    obj = Document(doc_path)
    for content in obj.paragraphs:
        title_level = content.style.name
        title = content.text

        if re.match("^Heading 6", title_level):
            if str(title) == 'RES_IP_AAA_DEV_查询记账方案_API':
                api_list.append(title)
                # print(title)
                break
            else:
                # print(title)
                api_list.append(title)
    print(f'我测了{len(api_list)}个，核对是否正确')
    return api_list


def get_json():
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def write_json(content):
    with open('附加测试.json', 'a+', encoding='utf-8') as fs:
        fs.write(content)
        fs.write(",\n")


def filter_json():
    my_json = get_json()
    api_name_list = get_my_api_name()
    for item in my_json['item']:
        if api_name_list.__contains__(str(item['name'])):
            # print(item, end=",\n")
            str_json = json.dumps(item, indent=4, ensure_ascii=False)
            write_json(str_json)
            # for it in item:
            #     print(f'{it} -- {item[it]}')


filter_json()
