
# else可与for 和 while搭配使用  当 循环正常结束（非break和异常结束） 会执行else的语句

for i in range(3):
    print('hhh')
else:
    print("end")

i = 3
while i > 0:
    i -= 1
    print(i)
else:
    print('end3')