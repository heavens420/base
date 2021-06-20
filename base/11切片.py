lst = ['u', 'y', 't', 'r', 'e', 'w', 'q']

# 左闭右开
print(lst[1:3])

# 设置步长为 2
print(lst[1:5:2])

# -1代表逻辑上的最后一位（包含最后一位）
print(lst[1:-1])

# start默认为0 end 默认为-1 step默认为 1
print(lst[::])

# 步长为 -1 从后往前
print(lst[6::-1])

# 步长为 负 结果包含最后一位
print(lst[5::-2])
