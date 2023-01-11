import os
import json


def analysis_json(file):
    with open(file, encoding='utf-8') as f:
        print(f.read)
        name_list = json.load(f)
    return name_list.get('data')


def print_for(name_list):
    for org in name_list:
        org_name = org.get("name")
        if org_name is not None:
            print(f'{org_name}',end='\n')
        else:
            org_name = org.get("username")
            print(f'{org_name}',end='\t')

        org_list = org.get('children')
        if org_list is not None and len(org_list) > 0:
            # print('-',end='')
            # print('组成1：', end='')
            for emp in org_list:
                emp_child = emp.get('children')
                if emp_child is not None:
                    # print()
                    print(f'{emp.get("name")}', end='\n')
                    print_for(emp_child)
                else:
                    print(f'{emp.get("username")}', end='\t')
            print()


if __name__ == '__main__':
    file_path = r'./name_list.json'
    name_list = analysis_json(file_path)
    print_for(name_list)
