from hdfs import InsecureClient

client = InsecureClient("http://10.142.101.156:50070", "hadoop")
files = client.list("/")
print(files)