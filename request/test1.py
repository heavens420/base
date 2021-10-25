import requests as req
import json

data = '''
{
    "MsgHead": {
        "MsgId": "1232",
        "MsgFrom": "default",
        "SendTime": "2021-09-27 15:18:29"
    },
    "MsgBody": {
        "ServParams": {
            "DownPort": "0-0-4-0",
            "loid": "hljgc0400",
            "card_type": "GPON",
            "Onuip": "",
            "ontid": "127"
        },
        "NeVendorCode": "",
        "AreaCode": "455",
        "NeIp": "170.152.157.10",
        "OldServParams": {},
        "EwsId": "202109271518291674674"
    }
}
'''

url = "http://136.192.124.177:30004/res/pon/ddmTest"
data = json.dumps(data.encode("utf-8"))

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0"
}
resp = req.post(url, data=data, headers=headers)

print(resp.json())
