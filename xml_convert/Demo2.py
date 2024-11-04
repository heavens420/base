import io
import sys
import urllib.parse
import xml.etree.cElementTree as ET
import urllib.request as request
import json

# 中文乱码问题
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def getXpathValue(root, xPath) -> str:
    value = root.find(xPath)
    return value.text


def getXpathAttrib(root, xPath) -> str:
    value = root.find(xPath)
    return value.attrib


def parseXml(root):
    isReservOrder = getXpathValue(root, r'interfacemsg/public/isReservOrder')
    print(f'---------{isReservOrder}')


def getRequest():
    response = request.urlopen('http://localhost:8087/microservice/scriptOperation/initMapList')
    text = json.dumps(str(response))
    print(f'response type:{type(response)}')
    print("status : |%s msg: %s |version: %s" % (response.status, response.msg, response.version))
    print("headers：%s" % response.getheaders())
    # print(response.read().decode('utf-8'))


def getRequestWithHeader():
    headers = {
        'Token': 'e84d61b5766189dd710138b9e90ab1f3'
    }
    req = request.Request(url='http://localhost:8087/microservice/scriptOperation/initMapList', headers=headers)
    response = request.urlopen(req)
    print(f'response type:{type(response)}')
    print("status : |%s msg: %s |version: %s" % (response.status, response.msg, response.version))
    print("headers：%s" % response.getheaders())
    print(response.read().decode('utf-8'))


def getRequestWithParamGet():
    headers = {
        'Token': 'e84d61b5766189dd710138b9e90ab1f3'
    }
    data = {
        'id': 1,
        'clazz': 'SoApiInstOptLogEntity'
    }
    payload = urllib.parse.urlencode(data)
    req = request.Request(url='http://localhost:8087/microservice/scriptOperation/commonQuery?' + payload,
                          headers=headers)
    response = request.urlopen(req)
    print(response.read().decode('utf-8'))


def getRequestWithParamPost():
    headers = {
        'Token': 'e84d61b5766189dd710138b9e90ab1f3',
        'Content-Type': 'application/json'
    }
    data = {
        'party_type': 'true',
        'sharding_id': 3
    }
    # data = "dddd"
    data2 = {
        "clazz": 'SoApiInstOptLogEntity'
    }
    payload2 = urllib.parse.urlencode(data2)
    payload = urllib.parse.urlencode(data, encoding='utf-8').encode('utf-8')

    # post请求传字符串参数
    newData = bytes("dddd".encode('utf-8'))

    # payload = bytes(str(data).encode('utf-8'))
    req = request.Request(url='http://localhost:8087/microservice/scriptOperation/testpost2',
                          headers=headers, data=payload)
    response = request.urlopen(req)
    print(response.read().decode('utf-8'))


if __name__ == '__main__':
    path = r'C:\Users\heave\Desktop\安徽智行云网项目\新文件 3.xml'
    # 脚本文件路径
    scriptName = sys.argv[0]
    # 脚本参数 即xml字符串
    script = sys.argv[1]
    print(f'脚本路径:{scriptName}')
    print(f'脚本参数：{script}')
    tree = ET.ElementTree(file=path)
    print(type(tree))
    print(type(tree.getroot()))
    # parseXml(tree.getroot())

    # getRequestWithParamPost()
