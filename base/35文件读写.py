'''
    文件读写 ： r 只读
              w 只写 文件不存在 新建
              a 以追加的方式打开，不存在则创建
              b 以二进制方式打开文件 读或写  需与 r w 同时使用
              + 以读写方式打开文件 需与其它模式一起使用 如 a+
'''

file = open(r'C:\workspace\python\w1\base\base\20字典操作-2.py', 'r')

file2 = open(r'C:\workspace\python\w1\base\base\io_test-1.txt', 'w')

file3 = open(r'C:\workspace\python\w1\base\base\io_test-1.txt', 'a')

file4 = open(r'C:\Users\420\Desktop\photo_2021-04-17_22-51-49.jpg', 'rb')

file2.write('hhhh')
file3.write('kite')
file5 = open(r'C:\workspace\python\w1\base\base\kk.jpg', 'wb')
file5.write(file4.read())

file.close()
file2.close()
file3.close()
file4.close()
file5.close()
