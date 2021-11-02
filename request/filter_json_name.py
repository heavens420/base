import json

json_path = r'C:\Users\420\Desktop\西藏集团考核测试\查询json\西藏-考核-IP-chaxun.json'


def get_json():
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def filter_name():
    api_list = get_json()
    for api in api_list['item']:
        name = api['name']
        print(name)


filter_name()
