import requests
import urllib.request as req

# get请求传参 params为传参，json形式
response = requests.get("http://httpbin.org/get", params={"id": "1"})
print(response.text)
print(response.url)

# post请求传参 data为传参 json形式
data = {"id": 1, "name": "hhhh"}
r2 = requests.post("http://httpbin.org/post", data=data)
print(r2.text)
print(r2.json())

# 发送put请求 data为传参 json形式
r3 = requests.put("http://httpbin.org/put", data=data)
print(r3.text)
# 修改默认编码
r3.encoding = "GBK"
# 查询当前编码
print(f'r3.encoding:{r3.encoding}')


