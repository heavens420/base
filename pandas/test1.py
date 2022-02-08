import pandas as pd
import random


def group_by_test():
    data = pd.read_csv("kk.csv", names=['a', 'b', 'c'], skiprows=0)

    print(data)
    print('-' * 30)
    res1 = data.groupby('b')
    print(res1.groups)
    print('-' * 30)
    print(res1.get_group(19))
    print('-' * 30)
    for age, option_age in res1:
        # print(age)
        print(option_age)
        print(f'---> {option_age.iloc[0]}')


def get_group_by():
    data = pd.read_csv("kk.csv", names=['a', 'b', 'c'], skiprows=0)
    result = data.groupby(['a'])
    for age, res in result:
        # print(res)
        # print('-'*30)
        with open('kks.csv', 'a+') as file:
            file.write(str(res.iloc[1]))


def gen_csv_data():
    random_name = ''.join(random.sample(
        ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e',
         'd', 'c', 'b', 'a'], 5))

    random_addr = ''.join(random.sample(
        ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e',
         'd', 'c', 'b', 'a'], 5))

    random_age = random.randint(1, 100)

    with open('kk.csv', 'a+') as file:
        file.write(f'{random_name},{random_age},{random_addr}\n')


if __name__ == '__main__':
    # for i in range(5000000):
    #     gen_csv_data()
    # get_group_by()
    group_by_test()