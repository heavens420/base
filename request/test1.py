import requests as req
import json

url = "http://135.64.134.201:30040/res/stn/pf/fanstatus/get"
data = {"deviceId": "101.248.0.94"}
# url = "http://135.64.134.201:30040/res/stn/pf/fanstatus/get?deviceId=101.248.0.94"
# data = {}

headers = {
    "Content-Type": "application/json;charset=UTF-8"
}
resp = req.request("get", url, headers=headers)

print(resp.json())
