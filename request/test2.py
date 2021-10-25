import requests
import json

headers = {
    'Content-Type': 'application/json;charset=UTF-8'
}
URI = "136.192.124.177:30004"

url = """
   http://{{URI}}/res/router/ctr/ip/routerdetailmodelcodequery   
"""
url = url.replace("{{URI}}", URI).replace("\n", "").replace("\r", "").strip()
print(url)
data = \
    {"extendInputParameter2": "[112.100.44.57]", "extendInputParameter1": "扩展入参1,预留扩展入参"}


def my_post():
    r = requests.post(url=url, headers=headers, json=data)
    result = r.json()
    result = json.dumps(result, indent=4, ensure_ascii=False)
    print(result)


my_post()
