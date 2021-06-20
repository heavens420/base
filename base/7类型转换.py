a = '88.8'
b = 77.3
c = True
d = '99'
e = 123

# 字符串小数同非整数字符串 无法转换为int
# print(int(a), type(int(a)))

# float 转int 小数位被舍弃
print(int(b), type(int(b)))

# 布尔转int True为1 False为0
print(int(c), type(int(c)))

# 字符串转int 只有整数数字类型可转
print(int(d), type(int(d)))

# 整数转float 末尾加.0
print(float(e), type(float(e)))
# 布尔转float 同整数转 float
print(float(c), type(float(c)))

