import io
import json
import sys

import requests

# 中文乱码问题
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# url_prefix = 'http://localhost:8095/microservice/'
url_prefix = 'http://192.168.226.86:8095/microservice/'


def getRedis(key: str, group: str) -> dict:
    url = url_prefix + 'getRedis'
    params = {'key': key, 'group': group}
    resp = requests.get(url, params=params)
    print(key, '-----resp.text------', resp.text)
    if resp is not None and resp.text is not None:
        return json.loads(resp.text)
    return {}


def setRedis(key: str, value: str, group: str, timeAlive=0):
    url = url_prefix + 'setRedis'
    params = {'key': key, 'value': value, 'group': group, 'time': timeAlive}
    resp = requests.get(url, params=params)


def apiOutParamInRedis(apiOutPram: str, resApiConfInfo: dict, custOrderId: int):
    print('---------apiOutPram---------', apiOutPram)
    print('---------resApiConfInfo---------', resApiConfInfo)
    print('---------custOrderId---------', custOrderId)
    url = url_prefix + 'apiOutParamInRedis'
    params = {'apiOutPram': apiOutPram, 'custOrderId': custOrderId}
    requests.post(url, params=params, json=resApiConfInfo)


def restartActivity(processInstId, activityInstId):
    url = url_prefix + 'restartActivity'
    params = {'processInstId': processInstId, 'activityInstId': activityInstId}
    requests.get(url, params=params)


def rollBackActivity(processInstId, activityInstId):
    url = url_prefix + 'rollBackActivity'
    params = {'processInstId': processInstId, 'activityInstId': activityInstId}
    requests.get(url, params=params)


def finishActivity(processInstId, activityInstId, policyCode):
    url = url_prefix + 'finishActivity'
    params = {'processInstId': processInstId, 'activityInstId': activityInstId, 'policyCode': policyCode}
    requests.get(url, params=params)


def rollBack(url, custOrderId):
    params = {'url': url, 'custOrderId': custOrderId}
    requests.get(url, params=params)


def dealBiz(mqInfo: dict):
    newOrOld = mqInfo.get('newOrOld')
    soAsyncData: dict = mqInfo.get('soAsyncData')
    # resApiInstId = ''
    # resultCode = ''
    policyCode = ''

    if 'new' == newOrOld:
        resApiInstId = soAsyncData.get('MsgHead').get('MsgId')
        resultCode = soAsyncData.get('MsgBody').get('ResultCode')
    else:
        resApiInstId = soAsyncData.get('APIINST')
        resultCode = soAsyncData.get('RESULTCODE')

    group = 'spring.redis.groupNames.soApiInst'
    apiInstDto = getRedis('api_inst_' + str(resApiInstId), group)
    resApiCode = apiInstDto.get('apiCode')
    apiVersion = apiInstDto.get('apiVersion')

    apiConfInfo = getRedis('so_api_' + str(resApiCode) + '_' + str(apiVersion), 'spring.redis.groupNames.soBaseConfig')

    processInstId = apiInstDto.get('processInstId')
    activityInstId = apiInstDto.get('activityInstId')

    branchPolicyList = apiConfInfo.get('branchPolicyList')

    if branchPolicyList is not None and len(branchPolicyList) > 0:
        policyCode = apiConfInfo.get('branchPolicyList')[0].get('policyCode')
        print('--------policyCode-------', policyCode)
    apiInstDto['apiOutparm'] = soAsyncData

    if ('200' == resultCode and 'new' == newOrOld) or ('0000' == resultCode and 'old' == newOrOld):
        orderId = apiInstDto.get('orderId')
        apiOutParamInRedis(str(soAsyncData), apiConfInfo, int(orderId))
        finishActivity(processInstId, activityInstId, policyCode)
        apiInstDto['dealState'] = 'S'
        apiInstDto['apiInstState'] = 'NORMAL'
        apiInstDto['dealResult'] = 'NORMAL'
        apiInstDto['expReasonCode'] = ''
        apiInstDto['expDesc'] = ''
    setRedis('api_inst_' + str(resApiInstId), str(apiInstDto), 'spring.redis.groupNames.soApiInst')
    # else:
    #     expDealPolicyList:list = apiConfInfo.get('expDealPolicyList')
    #     expDealActionCode = None
    #     expDealPolicy = {}
    #     for item in expDealPolicyList:
    #         if item.get('expCode') == resultCode:
    #             expDealActionCode = item.get('handleType')
    #             expDealPolicy = item
    #             break
    #
    #     if expDealActionCode is None:
    #         finishActivity(processInstId, activityInstId, policyCode)
    #         apiInstDto['dealState'] = 'F'
    #         apiInstDto['apiInstState'] = 'EXP_UNDEAL'
    #         apiInstDto['dealResult'] = 'MANUAL'
    #         apiInstDto['expReasonCode'] = resultCode
    #         apiInstDto['expDesc'] = '未查询到对应的处理策略'
    #
    #     if 'DATADEAL' == expDealActionCode:
    #         resApiCode = expDealActionCode.get('resApiCode')
    #         rfsApiCode = expDealActionCode.get('rfsApiCode')
    #         if resApiCode is not None:
    #             pass
    #         elif rfsApiCode is not None:
    #             pass
    #
    #


if __name__ == '__main__':
    jsonPath = sys.argv[1]
    # jsonPath = r'C:\Users\heave\Desktop\安徽智行云网项目\callback.json'
    print('-------jsonPath----', jsonPath)
    with open(jsonPath, 'r', encoding='utf-8') as file:
        mqInfo = json.loads(file.read())
    print('------mqInfo------', mqInfo)
    dealBiz(mqInfo)
