
# \t 在python中与前面的字符合占4个字符，前面已经占满4个字符，单独占4个字符
print('fluf\tjpdl')

# 此处占2个字符与前面fh合占4个字符
print('fh\tkl')

# \r 回车符号，后面的会覆盖前面的内容 fs被覆盖
print('fs\rfjal')

# \b 退格符号 后面的一个字符会覆盖前面的一个字符 f被覆盖
print('fakf\biii')

# \ 转义字符输出 \'hhh'
print('\\\'hhh\'')

# r 或 R 使字符自动转义,结尾不能是 \
print(r'\'hyy')
