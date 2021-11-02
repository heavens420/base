import re

ss = "nihaoa zheshijie" \
     "nidemingzi"
reg = r'jie'
# result = re.match(reg,ss)
# result = re.search(reg, ss)
# print(result.group())
# result = re.findall(reg, ss)
# print(result)

regx = re.compile(reg)
result = regx.search(ss)
print(result.group())
