# range() 左闭右开
r = range(10)

print(r)

print(list(r))

r2 = range(1, 10)

print(list(r2))

r3 = range(1, 10, 2)
print(list(r3))

print(10 in list(r2))

print(9 not in list(r2))
