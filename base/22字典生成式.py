names = ['apple', 'orange', 'banana']
prices = [12, 23, 34, 45, 56, 567]

# 字典生成 以元素少的列表为准
dic = {name: price for name, price in zip(names, prices)}

print(dic)
