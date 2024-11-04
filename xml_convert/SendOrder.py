import time
from datetime import datetime, date
import io
import sys
import xml.etree.cElementTree as ET
import json
import requests

# 中文乱码问题
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url_prefix = 'http://localhost:8087/microservice/'


def getCommonValue(root) -> dict:
    values = {}
    areaCode = root.find('interfacemsg/public/areaCode')
    values['areaCode'] = areaCode.text
    return values


def getXpathValue(root, xPath) -> str:
    value = root.findtext(xPath)
    return value


def getXpathAttrib(root, xPath) -> str:
    value = root.find(xPath)
    return value.attrib


def getPrimaryKey(tableName: str) -> int:
    url = url_prefix + 'scriptOperation/getPrimaryKey'
    params = {'tableName': tableName}
    response = requests.get(url, params=params)
    return int(response.text)


def getEnvProperties() -> dict:
    url = url_prefix + 'scriptOperation/getProperties'
    response = requests.get(url)
    print('---getEnvProperties---response------', response.text)
    return json.loads(response.text)


def getInitMapList() -> dict:
    url = url_prefix + 'scriptOperation/initMapList'
    response = requests.get(url)
    # print(f'res=={json.dumps(json.loads(response.text),indent=4,ensure_ascii=False)}')
    # print(type(json.loads(response.text)))
    return json.loads(response.text)


def setRedis(redisKey: str, redisJson, groupName=''):
    url = url_prefix + 'scriptOperation/setRedis'
    headers = {"Content-Type": "application/json;charset=utf-8"}
    params = {'redisKey': redisKey, 'groupName': groupName}
    print(redisKey, '-------------redisJson-------', redisJson)
    response = requests.post(url, json=redisJson, headers=headers, params=params)
    # return response.text


# orderRuleData：json字符串
def setMq(orderRuleData):
    url = url_prefix + 'scriptOperation/setMq'
    # data = {'orderRuleData': orderRuleData}
    headers = {"Content-Type": "application/json;charset=utf-8"}
    data = json.dumps(orderRuleData, ensure_ascii=False).encode('utf-8')
    response = requests.post(url, data=data, headers=headers)
    # return response.text


# json: 实体对象json字符串 clazz: 操作的实体对象类名
def insertBean(jsonData: dict, clazz: str):
    if jsonData is None or jsonData == {}:
        return
    for item in jsonData:
        # 针对时间类型格式特殊处理
        if isinstance(jsonData.get(item), datetime):
            jsonData[item] = jsonData[item].strftime('%Y-%m-%d %H:%M:%S')
    url = url_prefix + 'scriptOperation/insert'
    data = jsonData
    params = {'clazz': clazz}
    response = requests.post(url, json=data, params=params)
    return response.text


def createColCode(preFix: str, areaCode: str, suffix: str, hasDateStr: bool):
    dateStr = ''
    if hasDateStr:
        dateStr = str(datetime.now().strftime('%Y%m%d'))
    return preFix + areaCode + dateStr + suffix


bmCustOrderId = getPrimaryKey('bm_cust_order')
custId = getPrimaryKey('bm_cust')
ioMsgId = getPrimaryKey('io_msg')
omOrderId = getPrimaryKey('om_order')
bmProdInstId = getPrimaryKey('bm_prod_inst')
subBmprodInstId = getPrimaryKey('bm_prod_inst')
rmResAssignId = getPrimaryKey('rm_res_assign')
rmResAssignAttrId = getPrimaryKey('rm_res_assign_attr')
rmResAssignAttrId2 = getPrimaryKey('rm_res_assign_attr')

print('bmCustOrderId', bmCustOrderId)
print('custId', custId)
print('ioMsgId', ioMsgId)
print('omOrderId', omOrderId)
print('bmProdInstId', bmProdInstId)
print('subBmprodInstId', subBmprodInstId)
print('rmResAssignId', rmResAssignId)
print('rmResAssignAttrId', rmResAssignAttrId)
print('rmResAssignAttrId2', rmResAssignAttrId2)

# 分片
shardingId = bmCustOrderId % int(getEnvProperties().get('dbdn'))
print('-----shardingId---------', shardingId)


def bmCustOrder(root):
    bean = {}
    elements = root.findall('interfacemsg/cust_info/cust_info')
    fromSys = root.find('route/from').text
    acceptDate = root.find('route/time').text
    areaCode = getCommonValue(root).get('areaCode')

    for item in elements:
        if item.attrib['code'] == 'crm_cust_order_code':
            bean['custOrderCode'] = item.attrib['value']
            break
    bean['lastOptDate'] = datetime.now()
    bean['areaCode'] = areaCode
    bean['custOrderNo'] = bean.get('custOrderCode')
    bean['custSoNum'] = '1'
    bean['currentSoNum'] = '1'
    bean['custId'] = custId
    bean['custOrderState'] = '10Q'
    # 智慧诊断系统
    if fromSys == 'diagnosis':
        # 诊断单
        bean['orderType'] = '10DX'
    else:
        # 正常单
        bean['orderType'] = '10A'
    bean['shardingId'] = shardingId
    bean['isCore'] = '10N'
    bean['custOrderPriority'] = '10N'
    bean['orgCode'] = bean['areaCode']
    bean['custOrderId'] = bmCustOrderId
    if bean.get('custOrderCode') is None:
        custOrderCode = createColCode('CO', areaCode, str(bmCustOrderId), True)
        bean['custOrderCode'] = custOrderCode
        bean['custOrderNo'] = custOrderCode

    if acceptDate is not None:
        bean['acceptDate'] = acceptDate

    bean['createDate'] = datetime.now()
    bean['custOrderStateDate'] = datetime.now()
    bean['ioMsgId'] = ioMsgId

    insertBean(bean, 'BmCustOrderEntity')
    setRedis('bm_cust_order_' + str(bmCustOrderId), bean, groupName='spring.redis.groupNames.soCustOrder')


def bmCust(root):
    bean = {}
    elements = root.findall('interfacemsg/cust_info/cust_info')
    for item in elements:
        code = item.attrib.get('code')
        value = item.attrib.get('value')
        if code == "CUST_NAME_NEW":
            bean['custName'] = value
        if code == "cust_idno":
            bean['certNbr'] = value
        if code == "CUST_CODE":
            bean['custCode'] = value
        if code == "CUST_GRADE_ID":
            bean['custGrade'] = value
        if code == "cust_source":
            bean['custSort'] = value
        if code == "CUST_TYPE":
            bean['custType'] = value
    bean['custManager'] = ''
    bean['custAddress'] = ''
    bean['shardingId'] = shardingId
    bean['createdDate'] = datetime.now()
    bean['custId'] = custId
    insertBean(bean, 'BmCustEntity')


def bmCustLinkMan(root):
    bean = {}
    elements = root.findall('interfacemsg/prodInfo/prodCharacters/prodCharacter')
    if elements is not None:
        for item in elements:
            characterId = item.find('characterId').text
            characterValue = item.find('characterValue').text
            if characterId == '600067':
                bean['name'] = characterValue
            if characterId == '600068':
                bean['mobilePhone'] = characterValue
                bean['officePhone'] = characterValue
    bean['custId'] = custId
    bean['sex'] = ''
    bean['shardingId'] = shardingId
    insertBean(bean, 'BmCustLinkmanEntity')


def omOrder(root):
    bean = {}
    areaCode = getCommonValue(root).get('areaCode')
    orderCode = root.find('interfacemsg/public/orderCode').text
    key = root.find('interfacemsg/prodInfo/prodId').text + '-' + root.find('interfacemsg/prodInfo/soTypeId').text
    orderType = root.find('interfacemsg/public/workType').text
    service = getInitMapList().get(key)

    print(f'--------service---------{service}')
    bean['areaCode'] = areaCode
    bean['orderCode'] = orderCode
    bean['custOrderId'] = bmCustOrderId
    if service is not None:
        bean['serviceId'] = service.get('id')
        bean['serviceName'] = service.get('name')
    bean['orderPriority'] = '10N'
    bean['orderClass'] = '10S'
    bean['orderType'] = orderType
    if orderType == '10M':
        bean['orderState'] = '10MI'
    else:
        bean['orderState'] = '10Q'
    bean['state'] = '20V'
    bean['orderTitle'] = '5G移动产品定单' + str(int(datetime.now().timestamp()))
    bean['orderId'] = omOrderId
    if orderCode is None:
        bean['orderCode'] = createColCode('O', areaCode, str(omOrderId), True)
    bean['shardingId'] = shardingId
    bean['acceptDate'] = datetime.now()
    bean['createDate'] = datetime.now()
    bean['stateDate'] = datetime.now()
    print('-----------OmOrderEntity--------', bean)
    insertBean(bean, 'OmOrderEntity')


def bmServiceOrder(root):
    bean = {}
    initMap = getInitMapList()
    soType = root.find('interfacemsg/public/workType').text
    prodId = root.find('interfacemsg/prodInfo/prodId').text
    crmSoId = root.find('interfacemsg/public/orderCode').text
    elements = root.findall('interfacemsg/prodInfo/prodCharacters/prodCharacter')
    prodInfoMap = initMap.get('prodInfoMap')
    bean['orderId'] = omOrderId
    bean['custOrderId'] = bmCustOrderId
    bean['soType'] = soType
    bean['prodId'] = prodInfoMap.get(prodId).get('prodId')

    for item in elements:
        characterId = item.find('characterId').text
        characterValue = item.find('characterValue').text
        if characterId == "000011":
            if characterValue is None:
                characterValue = item.find('oldCharacterValue').text
            bean['accNbr'] = characterValue
            break
    bean['crmSoId'] = crmSoId
    bean['shardingId'] = shardingId
    print('-----------BmServiceOrderEntity-----', bean)
    insertBean(bean, 'BmServiceOrderEntity')


def bmProdInst(root):
    mianProductDtoList = []
    elements = root.findall('interfacemsg/prodInfo')
    initMap = getInitMapList()
    prodInfoMap = initMap.get('prodInfoMap')

    for item in elements:
        prodId = item.find('prodId').text
        eventId = item.find('eventId').text
        soTypeId = item.find('soTypeId').text
        bean = {}
        bean['orderId'] = omOrderId
        bean['prodId'] = prodInfoMap.get(prodId).get('prodId')
        event: dict = initMap.get('bmEventVOMap').get(soTypeId)
        print('event=======', event)
        if event is not None:
            bean['eventId'] = event.get('eventId')
            bean['eventCode'] = event.get('eventCode')
            bean['eventName'] = event.get('eventName')
        custElements = root.findall('interfacemsg/cust_info/cust_info')
        for item in custElements:
            code = item.attrib.get('code')
            value = item.attrib.get('value')
            if code == 'crm_prod_inst_id':
                bean['crmProdInstId'] = value
                break
        bean['mainFlag'] = '1'
        bean['prodCode'] = prodId
        bean['prodName'] = prodInfoMap.get(prodId).get('prodName')
        bean['shardingId'] = shardingId
        bean['prodInstId'] = bmProdInstId
        print('------------------BmProdInstEntity-------------', bean)
        insertBean(bean, 'BmProdInstEntity')
        bean['eventId'] = eventId
        prodInstAttr = bmProdInstAttr(root, bean)
        mianProductDtoList.append(prodInstAttr)
    return mianProductDtoList


def bmProdInstAttr(root, bmProdInstBean: dict):
    mainProductAttrDtoList = list()
    initMap = getInitMapList()
    prodAttrMap = initMap.get('prodAttrMap')

    elements = root.findall('interfacemsg/prodInfo/prodCharacters/prodCharacter')
    if elements is not None:
        for item in elements:
            characterId = item.find('characterId').text
            characterValue = item.find('characterValue').text
            oldCharacterValue = item.find('oldCharacterValue').text
            actType = item.find('actType').text
            bean = {}
            bean['prodInstId'] = bmProdInstId
            characterDictVO = prodAttrMap.get(characterId)
            if characterDictVO is None:
                continue
            bean['attrId'] = characterDictVO.get('attrId')
            bean['attrName'] = characterDictVO.get('attrName')
            bean['id'] = characterDictVO.get('id')
            bean['attrValue'] = characterValue
            bean['oldAttrValue'] = oldCharacterValue
            bean['actType'] = actType
            bean['attrCode'] = characterId
            bean['shardingId'] = shardingId
            print('---------------BmProdInstAttrEntity-----------', bean)
            insertBean(bean, 'BmProdInstAttrEntity')

            mainProductAttrDto = {}
            mainProductAttrDto['mainProductAttrCode'] = characterId
            mainProductAttrDto['mainProductAttrAction'] = actType
            mainProductAttrDto['mainProductAttrNewValue'] = characterValue
            mainProductAttrDto['mainProductAttrOldValue'] = oldCharacterValue
            mainProductAttrDtoList.append(mainProductAttrDto)
        bmProdInstBean['mainProductAttrDtoList'] = mainProductAttrDtoList
        mianProductDto = bmProdInstOther(bmProdInstBean)
        return mianProductDto


def bmProdInstOther(bean: dict):
    mianProductDto = {}
    mianProductDto['mainProdCode'] = bean.get('prodCode')
    mianProductDto['mainActionCode'] = bean.get('eventCode')
    mianProductDto['mainProductAttrDtoList'] = bean.get('mainProductAttrDtoList')
    mianProductDto['mainEventActCode'] = bean.get('eventId')
    return mianProductDto


def bmProdInstSub(root):
    subProductDtoList = []
    elements = root.findall('interfacemsg/subproducts/subproduct')
    initMap = getInitMapList()
    prodInfoMap = initMap.get('prodInfoMap')
    bmEventVOMap = initMap.get('bmEventVOMap')

    if elements is not None:
        for item in elements:
            subProductId = item.findtext('subProductId')
            actType = item.findtext('actType')
            print('-------subProductId---', subProductId)
            print('-------actType---', actType)
            event = bmEventVOMap.get(actType)

            bean = {}
            bean['orderId'] = omOrderId
            bean['prodId'] = prodInfoMap.get(subProductId).get('prodId')
            if bean.get('prodId') == -1:
                continue
            bean['eventId'] = event.get('eventId')
            bean['eventCode'] = event.get('eventCode')
            bean['eventName'] = event.get('eventName')
            bean['crmProdInstId'] = subProductId
            bean['mainFlag'] = '0'
            bean['prodCode'] = subProductId
            bean['prodName'] = prodInfoMap.get(subProductId).get('prodName')
            bean['shardingId'] = shardingId
            bean['prodInstId'] = subBmprodInstId
            print('----------------BmProdInstEntity--sub----', bean)
            insertBean(bean, 'BmProdInstEntity')
            bmProdInstAttrSub(item, initMap, bean, subProductDtoList)
    return subProductDtoList


def bmProdInstAttrSub(node, initMap: dict, subProdInstAttr: dict, subProductDtoList: list):
    print('----------node-----', node.tag)
    padList = []
    subApd = {}
    elements = node.findall('prodCharacters/prodCharacter')
    prodAttrMap = initMap.get('prodAttrMap')

    if elements is not None:
        for item in elements:
            characterId = item.find('characterId').text
            characterValue = item.find('characterValue').text
            oldCharacterValue = item.find('oldCharacterValue').text
            actType = item.find('actType').text

            bean = {}
            bean['shardingId'] = shardingId
            bean['prodInstId'] = subBmprodInstId
            if characterId is not None and characterId != '':
                characterDictVO = prodAttrMap.get(characterId)
                if characterDictVO is None:
                    continue
                bean['attrId'] = characterDictVO.get('attrId')
                bean['attrName'] = characterDictVO.get('attrName')
                bean['prodInstId'] = subBmprodInstId
                bean['id'] = characterDictVO.get('id')
                bean['attrValue'] = characterValue
                bean['oldAttrValue'] = oldCharacterValue
                bean['actType'] = actType
                bean['attrCode'] = characterId
                bean['shardingId'] = shardingId
                print('------------------BmProdInstAttrEntity--sub--', bean)
                insertBean(bean, 'BmProdInstAttrEntity')

                mpad = {}
                mpad['adjunctProductAttrCode'] = characterId
                mpad['adjunctProductAttrAction'] = actType
                mpad['adjunctProductAttrNewValue'] = characterValue
                mpad['adjunctProductAttrOldValue'] = oldCharacterValue
                padList.append(mpad)
        subApd['adjunctActionCode'] = subProdInstAttr.get('eventCode')
        subApd['adjunctProdCode'] = subProdInstAttr.get('prodCode')
        subApd['adjunctProductAttrDtoList'] = padList
        subProductDtoList.append(subApd)


def bmAccessAndBmSoAccess(root):
    elements = root.find('interfacemsg/prodInfo/prodCharacters')
    pass


def rmResAssign(root):
    bean = {}
    bean['orderId'] = omOrderId
    bean['shardingId'] = shardingId
    bean['createdDate'] = datetime.now()
    bean['resAssignId'] = rmResAssignId
    insertBean(bean, 'RmResAssignEntity')


def rmResAssignAttr(root):
    resInfoDtoList = []
    bean = {}
    bean2 = {}
    attrValue = root.find('interfacemsg/resInfo/newRes/CDMA-lteimsi').text
    attrValue2 = root.find('interfacemsg/resInfo/newRes/CDMA-lteopc').text
    oldAttrValue = root.find('interfacemsg/resInfo/oldRes/CDMA-lteimsi').text
    oldAttrValue2 = root.find('interfacemsg/resInfo/oldRes/CDMA-lteopc').text

    bean['resAssignId'] = rmResAssignId
    bean['attrCode'] = 'CDMA-lteimsi'
    bean['attrName'] = '4G-IMSI'
    bean['attrValue'] = attrValue
    bean['oldAttrValue'] = oldAttrValue
    bean['shardingId'] = shardingId
    bean['id'] = rmResAssignAttrId

    bean2['resAssignId'] = rmResAssignId
    bean2['attrCode'] = 'CDMA-lteopc'
    bean2['attrName'] = '4G-OPC'
    bean2['attrValue'] = attrValue2
    bean2['oldAttrValue'] = oldAttrValue2
    bean2['shardingId'] = shardingId
    bean2['id'] = rmResAssignAttrId2

    insertBean(bean, 'RmResAssignAttrEntity')
    insertBean(bean2, 'RmResAssignAttrEntity')

    bean4 = {}
    bean5 = {}
    bean4['resId'] = 'CDMA-lteimsi'
    bean4['newResValue'] = attrValue
    bean4['oldResValue'] = oldAttrValue

    bean5['resId'] = 'CDMA-lteopc'
    bean5['newResValue'] = attrValue2
    bean5['oldResValue'] = oldAttrValue2

    resInfoDtoList.append(bean4)
    resInfoDtoList.append(bean5)

    elements = root.find('interfacemsg/resInfo//')
    if elements is not None:
        for item in elements:
            tag = item.tag
            value = item.text
            bean3 = {}
            bean3['resId'] = tag
            bean3['newResValue'] = value
            oldValue = root.find('interfacemsg/resInfo/oldRes/' + tag).text
            if oldValue is None:
                oldValue = ''
            bean3['oldResValue'] = oldValue
            resInfoDtoList.append(bean3)
    return resInfoDtoList


def ioMsg(root, xml: str):
    msgId = root.find('route/msg_id').text
    sender = root.find('route/Sender').text
    servCode = root.find('route/ServCode').text
    areaCode = getCommonValue(root).get('areaCode')

    bean = {}
    bean['ioId'] = ioMsgId
    bean['msgId'] = msgId
    bean['msgFrom'] = areaCode + sender
    bean['msgServCode'] = servCode
    bean['dealFlag'] = 1
    bean['areaCode'] = areaCode
    bean['requestContent'] = xml
    bean['receiveTime'] = datetime.now()
    bean['shardingId'] = shardingId
    bean['dealTime'] = datetime.now()
    bean['msgTime'] = datetime.now()
    bean['responseContent'] = ''
    bean['dealResult'] = ''
    bean['isReservOrder'] = ''
    bean['responseTime'] = datetime.now()
    insertBean(bean, 'IoMsgEntity')


def saveOmParaInfo(root) -> list:
    initMap = getInitMapList()
    omParaDefines: list = initMap.get('omParaDefines')
    env = getEnvProperties()
    isYw: bool = env.get('isYw')
    soTypeId = root.find('interfacemsg/prodInfo/soTypeId').text
    omParaInfos = []
    prodAttrDefineMap = {}
    subProdAttrDefineMap = {}
    subProdDefineMap = {}
    prodAttrActDefineMap = {}
    subProdAttrActDefineMap = {}
    pilotProdDefineMap = {}
    prodOfferDefine = {}
    prodOfferInstAttrDefine = {}
    subprodRelaAttrDefineMap = {}
    subProdAttrActDefineMapOther = {}

    for omParaDefine in omParaDefines:
        paraClass = omParaDefine.get('paraClass')
        northParaCode = omParaDefine.get('northParaCode')
        northParaPath = omParaDefine.get('northParaPath')
        # print('---------------paraClass---------------', paraClass)
        # print('---------------northParaCode---------------', northParaCode)
        # print('---------------northParaPath---------------', northParaPath)
        if paraClass is None or paraClass == '':
            continue
        elif paraClass == '4':
            prodAttrDefineMap[northParaCode] = omParaDefine
        elif paraClass == '6':
            subProdAttrDefineMap[northParaCode] = omParaDefine
        elif paraClass == '5':
            subProdDefineMap[paraClass] = omParaDefine
        elif paraClass == '11':
            prodAttrActDefineMap[paraClass] = omParaDefine
        elif paraClass == '15':
            subProdAttrActDefineMap[paraClass] = omParaDefine
        elif paraClass == '16':
            subProdAttrActDefineMapOther[paraClass] = omParaDefine
        elif paraClass == '13':
            pilotProdDefineMap[paraClass] = omParaDefine
        elif paraClass == '14':
            subprodRelaAttrDefineMap[paraClass] = omParaDefine
        elif paraClass == '7':
            prodOfferDefine[paraClass] = omParaDefine
        elif paraClass == '8':
            prodOfferInstAttrDefine[paraClass] = omParaDefine
        elif paraClass == '9':
            if northParaPath is None or northParaPath == '':
                continue

            if '/newRes/' in str(northParaPath):
                omParaInfo = {}
                paraValue = root.find('interfacemsg/' + northParaPath).text
                paraOldValue = root.find('interfacemsg/' + str(northParaPath).replace('/newRes/', '/oldRes/')).text
                # omParaInfo['orderId']  = bmCustOrderId
                # omParaInfo['paraId'] = omParaDefine.get('paraId')
                # omParaInfo['paraCode'] = omParaDefine.get('paraCode')
                # omParaInfo['paraName'] = omParaDefine.get('paraName')
                # omParaInfo['paraClass'] = omParaDefine.get('paraClass')
                # omParaInfo['paraValue'] = paraValue
                setOmParaInfo(omParaInfo, omParaDefine, paraValue)
                omParaInfo['shardingId'] = shardingId
                omParaInfo['paraOldValue'] = paraOldValue
                if isYw and (paraValue is None or paraValue == ''):
                    omParaInfo['paraValue'] = paraOldValue
                    omParaInfos.append(omParaInfo)
                elif isYw and (paraOldValue is None or paraOldValue == ''):
                    omParaInfo['paraOldValue'] = paraValue
                    omParaInfos.append(omParaInfo)
                else:
                    omParaInfos.append(omParaInfo)
        elif paraClass == '1':
            elements = root.findall('interfacemsg/cust_info/cust_info')
            for item in elements:
                code = item.attrib.get('code')
                value = item.attrib.get('value')
                if code == northParaCode:
                    omParaInfo = {}
                    setOmParaInfo(omParaInfo, omParaDefine, value)
                    omParaInfo['shardingId'] = shardingId
                    omParaInfos.append(omParaInfo)
        else:
            if northParaPath is not None and northParaPath != '':
                value = root.findtext('interfacemsg/' + northParaPath)
                omParaInfo = {}
                setOmParaInfo(omParaInfo, omParaDefine, value)
                omParaInfo['shardingId'] = shardingId
                omParaInfos.append(omParaInfo)

    elements = root.findall('interfacemsg/prodInfo/prodCharacters/prodCharacter')

    if elements is not None:
        for item in elements:
            characterId = item.findtext('characterId')
            characterValue = item.findtext('characterValue')
            oldCharacterValue = item.findtext('oldCharacterValue')

            omParaDefine = prodAttrDefineMap.get(characterId)
            if omParaDefine is None:
                continue
            omParaInfo = {}
            setOmParaInfo(omParaInfo,omParaDefine,characterValue)
            omParaInfo['shardingId'] = shardingId
            omParaInfo['paraOldValue']  =oldCharacterValue
            if soTypeId == 'A20' and 'GroupCardType' == omParaDefine.get('paraCode'):
                omParaInfos.append(omParaInfo)
            else:
                paraOldValue = omParaInfo.get('paraOldValue')
                paraValue = omParaInfo.get('paraValue')
                if isYw and (paraValue is None or paraValue == ''):
                    omParaInfo['paraValue'] = paraOldValue
                    omParaInfos.append(omParaInfo)
                elif isYw and (paraOldValue is None or paraOldValue == ''):
                    omParaInfo['paraOldValue'] = paraValue
                    omParaInfos.append(omParaInfo)
                else:
                    omParaInfos.append(omParaInfo)

    subElements = root.findall('interfacemsg/subproducts/subproduct')
    if subElements is not None:
        for item in subElements:
            subProductId = item.findtext('subProductId')
            if subProductId is not None:
                for key in subprodRelaAttrDefineMap.keys():
                    if subProductId in key:
                        subprodInstAttrNodeList = item.findall('prodCharacters/prodCharacter')
                        if subprodInstAttrNodeList is not None:
                            for subItem in subprodInstAttrNodeList:
                                characterId = subItem.findtext('characterId')
                                omParaDefine = prodAttrDefineMap.get(subProductId + '-' + characterId)
                                characterValue = subItem.findtext('characterValue')
                                if omParaDefine is None:
                                    continue
                                omParaInfo = {}
                                setOmParaInfo(omParaInfo, omParaDefine, characterValue)
                                omParaInfo['shardingId'] = shardingId
                                omParaInfos.append(omParaInfo)
                        break
                for key in subProdAttrActDefineMapOther.keys():
                    if subProductId in key:
                        subprodInstAttrNodeList = item.findall('prodCharacters/prodCharacter')
                        if subprodInstAttrNodeList is not None:
                            for subItem in subprodInstAttrNodeList:
                                characterId = subItem.findtext('characterId')
                                omParaDefine = prodAttrDefineMap.get(subProductId + '-' + characterId)
                                act_type = subItem.findtext('act_type')
                                if omParaDefine is None:
                                    continue
                                omParaInfo = {}
                                setOmParaInfo(omParaInfo, omParaDefine, act_type)
                                omParaInfo['shardingId'] = shardingId
                                omParaInfos.append(omParaInfo)
                        break
            omProdParaDefine = subProdDefineMap.get(subProductId)
            if omProdParaDefine is None:
                continue
            omProdParaInfo = {}
            setOmParaInfo(omProdParaInfo, omProdParaDefine, subProductId)
            omProdParaInfo['shardingId'] = shardingId
            omParaInfos.append(omProdParaInfo)

            actTypeDefine = subProdDefineMap.get(subProductId + "-ActType")
            if actTypeDefine is not None:
                omProdActInfo = {}
                actType = item.findtext('actType')
                setOmParaInfo(omProdActInfo, actTypeDefine, actType)
                omProdActInfo['shardingId'] = shardingId
                omParaInfos.append(omProdActInfo)
            subprodInstAttrNodeList = item.findall('prodCharacters/prodCharacter')
            if subprodInstAttrNodeList is not None:
                for subItem in subprodInstAttrNodeList:
                    characterId = subItem.find('characterId').text
                    characterValue = subItem.find('characterValue').text
                    oldCharacterValue = subItem.find('oldCharacterValue').text
                    omParaDefine = prodAttrDefineMap.get(characterId)
                    paraCode = omParaDefine.get('paraCode')
                    omParaInfo = {}
                    if omParaDefine is None:
                        continue
                    setOmParaInfo(omParaInfo, omParaDefine, characterValue)
                    omParaInfo['shardingId'] = shardingId
                    omParaInfo['paraOldValue'] = oldCharacterValue
                    if soTypeId == 'A20' and paraCode == 'GroupCardType':
                        omParaInfos.append(omParaInfo)
                        continue
                    else:
                        paraOldValue = omParaInfo.get('paraOldValue')
                        paraValue = omParaInfo.get('paraValue')
                        if isYw and (paraValue is None or paraValue == ''):
                            omParaInfo['paraValue'] = paraOldValue
                            omParaInfos.append(omParaInfo)
                        elif isYw and (paraOldValue is None or paraOldValue == ''):
                            omParaInfo['paraOldValue'] = paraValue
                            omParaInfos.append(omParaInfo)
                        else:
                            omParaInfos.append(omParaInfo)

    omProdParaInfo = {}
    omProdParaInfo['orderId'] = bmCustOrderId
    omProdParaInfo['paraId'] = 10020905
    omProdParaInfo['paraCode'] = 'OrderId'
    omProdParaInfo['paraName'] = '定单号'
    omProdParaInfo['paraClass'] = '9'
    omProdParaInfo['paraValue'] = bmCustOrderId
    omProdParaInfo['shardingId'] = shardingId
    omParaInfos.append(omProdParaInfo)

    return omParaInfos


def setOmParaInfo(omParaInfo: dict, omParaDefine: dict, paraValue):
    omParaInfo['orderId'] = bmCustOrderId
    omParaInfo['paraId'] = omParaDefine.get('paraId')
    omParaInfo['paraCode'] = omParaDefine.get('paraCode')
    omParaInfo['paraName'] = omParaDefine.get('paraName')
    omParaInfo['paraClass'] = omParaDefine.get('paraClass')
    omParaInfo['paraValue'] = paraValue


def setOmParaInfo2(listOmParaInfoDto: list, paraId, paraCode, paraName, paraClass, paraValue):
    omProdParaInfo = {}
    omProdParaInfo['orderId'] = bmCustOrderId
    omProdParaInfo['paraId'] = paraId
    omProdParaInfo['paraCode'] = paraCode
    omProdParaInfo['paraName'] = paraName
    omProdParaInfo['paraClass'] = paraClass
    omProdParaInfo['paraValue'] = paraValue
    omProdParaInfo['shardingId'] = shardingId
    listOmParaInfoDto.append(omProdParaInfo)


def omParaInfo(root):
    esbId = root.find('route/EsbId').text
    fromSys = root.find('route/from').text

    listOmParaInfoDto = saveOmParaInfo(root)
    print('---------------listOmParaInfoDto-----------', listOmParaInfoDto)
    setOmParaInfo2(listOmParaInfoDto, 1, 'sg_id', '消息ID', '9', str(ioMsgId))
    setOmParaInfo2(listOmParaInfoDto, 3, 'EsbId', 'OIP流水号', '9', esbId)
    setOmParaInfo2(listOmParaInfoDto, 2, 'priority_flag', '优先级标识', '9', "")
    setOmParaInfo2(listOmParaInfoDto, 4, 'fromSys', '定单来源系统', '9', fromSys)
    if fromSys == 'pl_diagnosis':
        setOmParaInfo2(listOmParaInfoDto, 4, 'plDiagnosis', '批量诊断标识', '9', "Y")
    for item in listOmParaInfoDto:
        insertBean(item, 'OmParaInfoEntity')
    setRedis('om_para_info_' + str(bmCustOrderId), listOmParaInfoDto)

    msgMap = {}
    for item in listOmParaInfoDto:
        paraValue = item.get('paraValue')
        paraCode = item.get('paraCode')
        paraOldValue = item.get('paraOldValue')

        if paraValue is not None and paraValue != '':
            msgMap[paraCode] = paraValue
        if paraOldValue is not None and paraOldValue != '':
            msgMap['Old' + paraCode] = paraOldValue
    redisKey = 'so_orderparam_' + str(bmCustOrderId)
    setRedis(redisKey, msgMap)


# class ComplexEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, datetime):
#             return obj.strftime('%Y-%m-%d %H:%M:%S')
#         elif isinstance(obj, date):
#             return obj.strftime('%Y-%m-%d')
#         else:
#             return json.JSONEncoder.default(self, obj)


def parseXml(root, xml: str):
    bmCustOrder(root)
    bmCust(root)
    bmCustLinkMan(root)
    omOrder(root)
    bmServiceOrder(root)
    mianProductDtoList = bmProdInst(root)
    subProductDtoList = bmProdInstSub(root)
    bmAccessAndBmSoAccess(root)
    rmResAssign(root)
    resInfoDtoList = rmResAssignAttr(root)
    ioMsg(root, xml)
    omParaInfo(root)

    values = getCommonValue(root)
    areaCode = values.get('areaCode')
    esbId = root.find('route/EsbId').text
    servCode = root.find('route/ServCode').text
    msgId = root.findtext('route/msg_id')
    orderAttrListDto = {}
    roIomDto = {}
    roIomDto['msgId'] = msgId
    roIomDto['areaCode'] = areaCode
    roIomDto['esbId'] = esbId
    roIomDto['phoneNumber'] = ''
    roIomDto['receiveTime'] = time.time()
    roIomDto['servCode'] = servCode
    orderAttrListDto['roIomDto'] = roIomDto
    orderAttrListDto['orderId'] = bmCustOrderId
    orderAttrListDto['orderTitle'] = '5G移动产品客户定单' + str(time.time())
    orderAttrListDto['resInfoDtoList'] = resInfoDtoList
    orderAttrListDto['mianProductDtoList'] = mianProductDtoList
    orderAttrListDto['adjunctProductDtoList'] = subProductDtoList

    print('--------orderAttrListDto------', str(orderAttrListDto))
    setMq(orderAttrListDto)


if __name__ == '__main__':
    # path = sys.argv[0]
    # xml = sys.argv[1]
    # print('-----xml-----', xml)
    # path = r'C:\Users\heave\Desktop\安徽智行云网项目\新文件 3.xml'
    path = sys.argv[1]
    print('-------path-----', path)
    with open(path, 'r', encoding='utf-8') as file:
        xml = file.read()
    print('-' * 50)
    print(xml)
    # parser = ET.XMLParser(encoding="utf-8")
    tree = ET.ElementTree(file=path)
    # root = ET.fromstring(xml, parser=parser)
    root = tree.getroot()
    parseXml(root, xml)

    # print(len(root.findall('interfacemsg')))
    # print(datetime.datetime.now())
    # print(ss.get('dd'))
    # print(shardingId)
    # print(createColCode('sd', '999', '111', True))
    # bmCustLinkMan(root)

    # print(datetime.now().timestamp())
    # omOrder(root)

    # print(type(datetime.now()))
    # elements = root.find('interfacemsg/resInfo//')
    # items = elements.items()
    # keys = elements.keys()
    # itor = elements.getiterator()
    # children = elements.getchildren()
    #
    # for key in items:
    #     print(key.)

    # for item in elements:
    #     print(f'---{item.tag}')
    # ss = {'id':33,'name':'ffff','addr':'ttt','time':datetime.now()}
    # print(str(ss))
    # setMq('333')
