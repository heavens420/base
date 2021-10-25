from hdfs import InsecureClient
from pyhdfs import HdfsClient
import os
client = InsecureClient("http://192.168.80.220:50070", user="hadoop")

# print(dir(InsecureClient))
total = 0

for root, dirs, files in client.walk("/test", status=True):
    print(f'root->{root}')
    # print(f'dirs->{dirs}')
    print(f'file->{files}')
    for item in files:
        total += item[1]["length"]
    # print(total)

print(total)


# file = client.list("/test", status=True)
# print(file)

def sum_file(path):
    for root, dirs, files in client.walk(path, status=True):
        print(f'root->{root}')
        # print(f'dirs->{dirs}')
        # print(f'file->{files}')
        for item in files:
            total += item[1]["length"]
