import json

'''
    按行读取文本内容 将每行内容和json的item['name']比较过滤
'''

txt_path = r'C:\Users\420\Desktop\ipran.txt'
json_path = r'C:\Users\420\Desktop\IPRAN中期.json'


# 按行读取文件内容 返回列表
def read_file():
    with open(txt_path, 'r', encoding='utf-8') as file:
        return file.readlines()


# 获取json数据 json格式
def get_json():
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)


# 将过滤后的json写到新文件
def write_json(content):
    with open('chaxun.json', 'a+', encoding='utf-8') as fs:
        fs.write(content)
        fs.write(",\n")


def filter_json():
    api_name_list = read_file()
    my_json = get_json()

    for item in my_json['item']:
        if api_name_list.__contains__(str(item['name']) + '\n'):
            # print(item, end=",\n")
            str_json = json.dumps(item, indent=4, ensure_ascii=False)
            write_json(str_json)


filter_json()
