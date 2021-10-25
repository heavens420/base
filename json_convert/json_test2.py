import json


def get_json():
    path = r'C:\Users\420\Desktop\collection.json'
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


def filter_json():
    data = get_json()
    for item in data['item']:
        if str(item['name']).__contains__("查"):
            for it in item:
                print(f'{it} -- {item[it]}')
        # print(item)


filter_json()
