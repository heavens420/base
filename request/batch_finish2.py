import json
import sys

import requests

jsonParam = {
    "id": 3,
    "apiName": "故障智能分析回调API",
    "apiCode": "faultIntelligentAnalysisCallbackApi",
    "apiType": "操作",
    "apiCategory": "回调API",
    "apiAddr": "",
    "timeoutLimit": 100000,
    "interviewMode": "同步",
    "simulation": "否",
    "requestHead": "{}",
    "dataFormat": "json",
    "scriptType": "groovy",
    "inParamStructure": "{\n    \"newOrOld\": \"new\",\n    \"soAsyncData\": {\n        \"MsgHead\": {\n            \"MsgId\": \"#apiInstId#\", // apiInstId\n            \"RelMsgId\": \"\",\n            \"SendTime\": \"\",\n            \"MsgFrom\": \"\"\n        },\n        \"MsgBody\": {\n            \"ResultCode\": \"200\",\n            \"ResultDesc\": \"\",\n            \"ServResult\": {\n                \"ResultCode\": \"\",\n                \"ResultDesc\": \"\",\n                \"OrgReports\": \"\",\n                \"ServReports\": \"\"\n            }\n        }\n    }\n}",
    "inParamReflect": "{}",
    "outParamSimulation": "{}",
    "script1": "import com.alibaba.fastjson.JSONObject\nimport usi.dbdp.soasync.service.SoAsyncService\nimport usi.dbdp.soasync.util.SpringContextUtil\n\n\ndef execute() {\n    SoAsyncService soAsyncService = SpringContextUtil.applicationContext.getBean(SoAsyncService.class)\n    def map = $groovyParam\n    String soAsyncData = JSONObject.toJSONString(map.soAsyncData)\n    map.soAsyncData = soAsyncData\n    soAsyncService.dealBiz(JSONObject.toJSONString(map))\n}\n\nexecute()",
    "script": "//package usi.dbdp.soasync.service\n\n\nimport com.alibaba.fastjson.JSON\nimport com.alibaba.fastjson.JSONObject\nimport usi.dbdp.redis.CommonRedisUtil\nimport usi.dbdp.redis.ConstantForRedis\nimport usi.dbdp.redis.dto.ApiForRedis\nimport usi.dbdp.soasync.SoConstantForBwp\nimport usi.dbdp.soasync.dto.ApiInstDto\nimport usi.dbdp.soasync.dto.cnccCallBack.CnccCallBackMsgDto\nimport usi.dbdp.soasync.service.SoAsyncService\nimport usi.dbdp.soasync.util.ScriptBwpOperations\nimport usi.dbdp.soasync.util.SpringContextUtil\n\n//class CallBackOrder {\n\n\n// 入口函数 相当于main方法\ndef execute() {\n    CommonRedisUtil commonRedisUtil = SpringContextUtil.applicationContext.getBean(CommonRedisUtil.class)\n    ScriptBwpOperations scriptBwpOperations = SpringContextUtil.applicationContext.getBean(ScriptBwpOperations.class)\n    SoAsyncService soAsyncService = SpringContextUtil.applicationContext.getBean(SoAsyncService.class)\n\n    def map = $groovyParam\n    // Map<String, String> map = JSONObject.parseObject(mqInfo, Map.class)\n    println(\"================map=================\" + map)\n    String newOrOld = map.get(\"newOrOld\");\n    Map<String,Object> soAsyncData = map.get(\"soAsyncData\");\n    String resApiInstId = \"\";\n    String resultCode = \"\";\n\n    println(\"================newOrOld=================\" + newOrOld)\n    if (\"new\" == newOrOld) {\n        CnccCallBackMsgDto dto = JSON.parseObject(JSONObject.toJSONString(soAsyncData), CnccCallBackMsgDto.class);\n        println(\"===========dto========\" + JSONObject.toJSONString(dto))\n        resApiInstId = dto.getMsgHead().getMsgId();\n        resultCode = dto.getMsgBody().getResultCode();\n    }\n    // 当前API实例 for apiInst update\n    ApiInstDto apiInstDto = new ApiInstDto();\n\n    String resApiCode;\n    long processInstId;\n    long activityInstId;\n    String policyCode = null\n\n    try {\n        String apiInstStr = commonRedisUtil.getRedis(ConstantForRedis.API_INST + resApiInstId, ConstantForRedis.GROUP_NAME_SO_API_INST);\n        apiInstDto = JSON.parseObject(apiInstStr, ApiInstDto.class);\n        println(\"===========apiInstDto==========\" + JSONObject.toJSONString(apiInstDto))\n        resApiCode = apiInstDto.getApiCode();\n        ApiForRedis apiConfInfo = JSONObject.parseObject(commonRedisUtil.getRedis(ConstantForRedis.API + resApiCode + \"_\" + apiInstDto.getApiVersion(), ConstantForRedis.GROUP_NAME_SO_BASECONFIG), ApiForRedis.class);\n\n        processInstId = apiInstDto.getProcessInstId();\n        activityInstId = apiInstDto.getActivityInstId();\n        if (apiConfInfo.getBranchPolicyList() != null && apiConfInfo.getBranchPolicyList().size() > 0) {\n            println(\"==============getBranchPolicyList==================\" + JSONObject.toJSONString(apiConfInfo.getBranchPolicyList()))\n            policyCode = apiConfInfo.getBranchPolicyList().get(0).getPolicyCode()\n        }\n        // 解析异步服务包的报文\n        if ((\"200\" == resultCode && \"new\" == newOrOld) || (\"0000\" == resultCode && \"old\" == newOrOld)) {\n            // 结束环节\n            scriptBwpOperations.finishActivity(processInstId, activityInstId, policyCode)\n\n            apiInstDto.setDealState(SoConstantForBwp.S);\n            apiInstDto.setApiInstState(SoConstantForBwp.NORMAL);\n            apiInstDto.setDealResult(SoConstantForBwp.NORMAL);\n            apiInstDto.setExpReasonCode(\"\");\n            apiInstDto.setExpDesc(\"\");\n            apiInstDto.setSqlAction(\"update\")\n            soAsyncService.apiInstInMq(apiInstDto)\n//            activityService.finishActResResult(processInstId, activityInstId, SoConstantForBwp.USER, SoConstantForBwp.NORMAL);\n\n        } else {\n            throw new RuntimeException(\"=========error param===============\")\n        }\n    } catch (Exception e) {\n        println(\"==============================未知异常=======================\")\n        e.printStackTrace()\n        return e.getMessage()\n    }\n    return \"success\"\n}\n\nexecute()\n\n//}",
    "apiRemark": "fdf",
    "delFlag": 0
}


def get_api_inst_list() -> list:
    with open(path, 'r') as file:
        api_inst_list = file.readlines()
        # api_inst_list = file.read()
        # print(api_inst_list)
        return api_inst_list


def get_order_id_list() -> list:
    with open('txt/order_id_list.txt', 'r', encoding='utf-8') as file:
        # orders = file.read()
        # order_id_list = json.loads(orders)
        order_id_list = file.readlines()
        # print(f'order:{order_id_list}')
        return order_id_list


def get_running_api() -> list:
    with open(path, 'r', encoding='utf-8') as file:
        api_list_str = file.read()
        api_list: list = json.loads(api_list_str)
        # print(api_list[0])
        return api_list


def finish_activity(param):
    url = r'http://134.95.222.252:10431/microservice/faultIntelligentAnalysisCallbackApi'
    resp = requests.post(url, json=param)
    body = resp.text
    print('--' * 50)
    print(body)


# 手动回调
def batch_call_back():
    api_inst_list = get_running_api()
    inParam = jsonParam['inParamStructure']
    count = 0

    for api in api_inst_list:
        api_inst_id = api['api_inst_id']
        order_id = api['order_id']
        setCache(order_id)
        jsonParam['inParamStructure'] = inParam.replace('#apiInstId#', str(api_inst_id).replace('\n', ''))
        print(jsonParam)
        # print(type(jsonParam))
        # print(f'orderId:{order_id}')
        finish_activity(jsonParam)
        count += 1
        # break
    print(f'共执行了{count}个')


def getCache(orderId: str) -> str:
    cache_url = r'http://134.95.222.252:18519/microservice/getRedis'
    # cache_url = r'http://localhost:8095/microservice/getRedis'
    params = {'key': 'so_orderparam_', 'group': 'spring.redis.groupNames.soParamInfo'}
    # params['key'] = params['key'] + '391668'
    params['key'] = params['key'] + str(orderId)
    # print(f'key:{params["key"]}')
    body = requests.get(cache_url, params=params).text
    if body is None or body == '':
        body = "{}"
        print('--' * 100, params['key'])
    body = json.loads(body)
    body['perfOptCode'] = '2'
    # print(f'body:{body}')
    # print(f'value:{body["orderType"]}')
    return json.dumps(body, ensure_ascii=False)
    # return str(body)


def getApiInstCache(apiInstId: str):
    cache_url = r'http://134.95.222.252:18519/microservice/getRedis'
    # cache_url = r'http://localhost:8095/microservice/getRedis'
    params = {'key': 'api_inst_', 'group': 'spring.redis.groupNames.soApiInst'}
    # params['key'] = params['key'] + '391668'
    params['key'] = params['key'] + str(apiInstId)
    body = requests.get(cache_url, params=params).text
    return body


def setApiInstCache(apiInstId: str, value):
    cache_url = r'http://134.95.222.252:18512/microservice/cache/updateDate'
    data = {"key": "api_inst_", "value": json.dumps(value, ensure_ascii=False),
            "groupName": "group.4120316_206_OSS_ZXDN_CACHE_001.so_api_inst"}
    data['key'] = data['key'] + str(apiInstId)
    body = requests.post(cache_url, data=data, headers={'Token': 'ee1dfd9b0b3f992fef4dc269f43111eb'}).text
    print(f'body:{body}')


def re_set_cache():
    order_id_list = get_running_api()
    for api in order_id_list:
        apiInstId = str(api['api_inst_id']).replace('\n', '')
        value = getApiInstCache(apiInstId)
        print('orderId--------', api['order_id'])
        if value is None or value.strip() == "":
            param = {
                'apiClass': 'RES',
                'apiInstId': api['api_inst_id'],
                'apiInstName': api['api_inst_name'],
                'processInstId': api['process_inst_id'],
                'activityInstId': api['activity_inst_id'],
                'apiCode': api['api_code'],
                'apiVersion': api['api_version'],
                'orderId': api['order_id'],
                'apiType': api['api_type'],
                'dealState': api['deal_state'],
                'shardingId': api['sharding_id'],
                'outParam': "{\"ResultCode\":\"200\",\"body\":{\"resultCode\":\"0\",\"resultDesc\":\"成功\"}}",
                'sqlAction': 'insert'
            }
            setApiInstCache(apiInstId, param)
        # break


def setCache(orderId: str):
    cache_url = r'http://134.95.222.252:18519/microservice/setRedis'
    # cache_url = r'http://localhost:8095/microservice/setRedis'
    params = {'key': 'so_orderparam_', 'value': "", 'group': 'spring.redis.groupNames.soParamInfo', }
    params['key'] = params['key'] + str(orderId)
    value = getCache(orderId)
    # params['value'] = str(value).replace('\'', '\"')
    params['value'] = value
    # print(f'param:{params}')
    print(f'value:{params["value"]}')

    body = requests.post(cache_url, data=params)
    print(f'body:{body.text}')


# 设置缓存
def setCache2(orderId: str):
    value = getCache(orderId)
    cache_url = r'http://134.95.222.252:18512/microservice/cache/updateDate'
    data = {"key": "so_orderparam_", "value": value,
            "groupName": "group.4120316_206_OSS_ZXDN_CACHE_001.so_param_info"}
    data['key'] = data['key'] + str(orderId)
    body = requests.post(cache_url, data=data, headers={'Token': '4dcec7c5005d4881a4a4d16d8e982ca7'}).text
    print(f'body:{body}')


# 重启环节
def batch_restart_api():
    count = 0
    api_list = get_running_api()
    out_param = """
    {
    "ResultCode": "200",
    "code": "200",
    "data": {
        "desc": "业务恢复"
    },
    "reply": "正常"
}
    """
    for api in api_list:
        # api = dict(api)
        param = {
            'type': 'restart',
            'apiInstId': api['api_inst_id'],
            'processInstId': api['process_inst_id'],
            'activityInstId': api['activity_inst_id'],
            'apiCode': api['api_code'],
            'apiVersion': api['api_version'],
            'orderId': api['order_id'],
            'apiType': api['api_type'],
            'targetApiInstId': '',
            'shardingId': api['sharding_id'],
            # 'outParam': api['api_outparm'],
            'outParam': out_param,
            'dealRemark': ''
        }
        # setCache2(api['order_id'])
        # print(f'param:{param}')
        restart_url = r'http://134.95.222.252:10431/microservice/ae/handleResExp'
        body = requests.post(restart_url, data=param, headers={'Token': token}).text
        count += 1
        print(f'body:{body}')
        # break
    print(f'共执行了{count}个')


def testExe():
    with open(path, 'r', encoding='utf-8') as file:
        result = file.read()
        print(f'文件内容:\n{result}')


if __name__ == '__main__':
    cmdList = '''请输入对应序号：
1 批量重启
2 打印测试
3 退出
'''
    path = input('请输入txt文件路径:')
    print(f'你输入的文件路径:{path}')
    token = input('请输入token:')
    print(f'你输入的token:{token}')
    cmd = input(cmdList)
    while 1:
        try:
            if cmd == '1':
                batch_restart_api()
            elif cmd == '2':
                testExe()
            else:
                sys.exit(0)
            cmd = input('请选择功能：')
        except Exception as e:
            print(e)
            cmd = input('请选择功能：')

    # batch_call_back()
    # finish_activity(jsonParam)
    # getCache()
    # setCache()
    # setCache2()

    # batch_restart_api()
    # get_order_id_list()
    # re_set_cache()
