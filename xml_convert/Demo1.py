import xml.etree.cElementTree as ET

xml = '''
<data>
    <country name="Liechtenstein">
        <rank updated="yes">2</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rank updated="yes">5</rank>
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank updated="yes">69</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
    </country>
</data>
'''

filePath = r'C:\Users\heave\Desktop\安徽智行云网项目\新文件 3.xml'


def parseXml():
    tree = ET.ElementTree(file=filePath)

    # root = ET.fromstring(xml)
    print("xml树：", tree)
    # 读文件 需要getroot 读字符串直接得到root
    root = tree.getroot()

    for child in root:
        print(f'-------{child.tag}:{child.attrib}:{child.text}-----------')
        for child1 in child:
            print(f'--------2-------{child1.tag}:{child1.attrib}:{child1.text}------2--------')
        print(end='\n')


def xPathTest() -> None:
    root = ET.fromstring(xml)
    # 获取所有data/country/neighbor节点
    # elements = root.findall('country/neighbor')
    # find() 只找第一个
    elements = root.find('country')
    print(f'{elements.tag},{elements.text},{elements.attrib}')
    for child in elements:
        print(f'-------{child.tag}:{child.attrib}:{child.text}-----------')


def getXpathElements():
    tree = ET.ElementTree(file=filePath)
    root = tree.getroot()
    elements = root.findall('interfacemsg/cust_info/cust_info')
    print(f'root-------{root}:{root.text}')
    for child in elements:
        print(f'-------{child.tag}:{child.attrib}:{child.text}-----------')
        # print(child.attrib['value'])





if __name__ == '__main__':
    # parseXml()
    # xPathTest()
    getXpathElements()
