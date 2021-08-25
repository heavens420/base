import os
import time
import numpy as np
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from lxml.etree import Element, SubElement, tostring
from xml.etree.ElementTree import fromstring, ElementTree


def prettyXml(element, indent, newline, level=0):  # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
    if element:  # 判断element是否有子元素
        if element.text == None or element.text.isspace():  # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
            # else:  # 此处两行如果把注释去掉，Element的text也会另起一行
    # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element)  # 将elemnt转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1):  # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        prettyXml(subelement, indent, newline, level=level + 1)  # 对子元素进行递归操作
    return element


from xml.etree import ElementTree  # 导入ElementTree模块


def execute_format():
    tree = ElementTree.parse('original-激活.xml')  # 解析test.xml这个文件，该文件内容如上文
    root = tree.getroot()  # 得到根元素，Element类
    root = prettyXml(root, '\t', '\n')  # 执行美化方法
    # ElementTree.dump(root)  # 打印美化后的结果
    tree = ET.ElementTree(root)  # 转换为可保存的结构
    xml_save_name = "激活-format.xml"
    tree.write(xml_save_name, encoding='utf-8')  # 保存美化后的结果

    tree2 = ElementTree.parse('original-采控.xml')  # 解析test.xml这个文件，该文件内容如上文
    root2 = tree2.getroot()  # 得到根元素，Element类
    root2 = prettyXml(root2, '\t', '\n')  # 执行美化方法
    # ElementTree.dump(root2)  # 打印美化后的结果
    tree2 = ET.ElementTree(root2)  # 转换为可保存的结构
    xml_save_name2 = "采控-format.xml"
    tree2.write(xml_save_name2, encoding='utf-8')  # 保存美化后的结果

execute_format()