import json

'''
   字典转json数据用json.dumps()方法实现。相反，json转字典用json.loads()方法.
   json.loads() ,json.load() , json.dump(), json.dumps() 
'''

# path = r'C:\Users\420\Desktop\collection.json'
# path = r'C:\Users\420\Desktop\json_test.txt'
path = r'C:\Users\420\Desktop\json_test.json'


def get_json():
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)
        # return json.dumps(file,indent=4)


# print(get_json())
# print(type(get_json()))
# print(get_json().encode(encoding='utf-8'))

def for_dict():
    data = get_json()
    for item in data:
        # print(item)
        if item == "name":
            print(f'{item} -- {data[item]}')


for_dict()
