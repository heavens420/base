score = dict(name='nihao', age=12, addr='beijign')

# 遍历字典
for item in score:
    print(item, '-----', score[item], '----', score.get(item))
