# 集合元素相同则相同 不考虑顺序
s = set([1, 2, 3, 4])
s2 = set([4, 3, 2, 1])
print(s2 == s)


s3 = set([1,2,3,4,5,6,7])
# s 是否为 s3的子集
print(s.issubset(s3))

# s3是否为s的超集
print(s3.issuperset(s))

# 两个集合是否没有交集  没有为true  有为false
print(s.isdisjoint(s3))

