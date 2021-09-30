import requests as req

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
headers = {"Content-Type": "application/x-www-form-urlencoded"}
resp = req.post("http://136.192.124.177:30004/res/pon/ddmTest", data=data, headers=headers)

print(resp.json())
