import time

import pymysql
import os
import datetime
import re
import sys

'''
    数据下发功能，在数据备份服务器上执行此脚本
'''


def con():
    host = 'jing.tk'
    port = 3313
    username = 'root'
    passwd = 'ROOT#'
    db = 'data_back'
    conn = pymysql.connect(host=host, port=port, user=username, password=passwd, database=db, charset="utf8")
    # print(conn)
    conn.select_db("data_back")
    cursor = conn.cursor()
    return cursor, conn


# 查询数据库中 所有的系统信息
def find_system():
    cursor, conn = con()
    sql = f"select sys_name_chn,sys_name_eng,data_type_chn,data_type_eng from t_back_config where status_cd = 0;"
    cursor.execute(sql)
    sys_list = cursor.fetchall()
    conn.close()
    print(f"系统名称----------system code-------文件类型")
    for item in sys_list:
        print(f"{item[0]}-----{item[1]}-----{item[2]}-----{item[3]}")


# 根据system code或编码查询系统账期
def find_zq_by_sysid(sysid, data_type):
    cursor, conn = con()
    sql = f"select distinct log.zq from t_back_log log where log.sys_name_eng = '{sysid}'" \
          f"and log.status_cd = 0 and log.zq is not null"
    # 数据类型非空则作为查询条件
    if data_type != '':
        sql = sql + f" and log.data_type_eng = '{data_type}'"
    print(sql)

    cursor.execute(sql)
    zq_list = cursor.fetchall()
    conn.close()
    if len(zq_list) == 0:
        print(f"系统{sysid}无可用帐期！")
        print()
        return
    print(f"系统{sysid}的可用账期如下:")
    for item in zq_list:
        print(f"{item[0]}")
    print()


# 账期查询
def zq_query(promote):
    # 提示信息
    find_system()
    param = str(input(promote)).strip().split(",")

    data_type = ''
    if param[0] != '':
        sysid = str(param[0])
        if len(param) > 0:
            data_type = param[1]
        find_zq_by_sysid(sysid, data_type)
    else:
        zq_query(promote)
    # 返回系统编码
    return param[0]


# ------------------------------------

# 更新下发记录
def write_release_log(file_list):
    cursor, conn = con()
    for item in file_list:
        begin_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = f"insert into t_release_log(file_name,md5,send_begin_date) values ('{item[3]}','{item[2]}','{begin_date}')"
        cursor.execute(sql)
    # 更改操作 要提交
    conn.commit()
    conn.close()


# 数据下发
def release_file(sysid, zq):
    cursor, conn = con()
    # 根据系统编码和账期查询要下发的文件列表
    sql = f"select log.back_cycle,log.data_type_eng,log.md5 ,log.file_name from t_back_log log  where " \
          f"log.sys_name_eng = '{sysid}' and log.zq = '{zq}'"
    cursor.execute(sql)
    zq_list = cursor.fetchall()
    conn.close()

    if zq_list is None:
        print("当前系统下无可下发账期！")
        return

    if len(zq) == 14:
        # 根据账期截取 当前账期文件目录
        zq_dir = zq_list[0][0] + zq[:8] + "000000"
        # 复制当前账期的整个文件夹到下发服务器
        cmd = f"scp -P 54321 -r /usr/local/data_back/store/{sysid}/{zq_list[0][1]}/{zq_dir}/ root@jing.tk:/usr/local/my/download/{sysid}/"
        res = os.system(cmd)
        if res == 0:
            print(f"{sysid}系统的{zq}账期下发成功！")
            # 记录日志
            write_release_log(zq_list)
        else:
            print("数据下发失败，请重新下发！")
    else:
        print(f"系统{sysid}下没有有效账期！")


def execute():
    print("可用功能:")
    print("1 账期查询")
    print("2 数据下发")
    print("3 退出")
    print()
    options = input("请输入功能编号:")
    if options.strip() == '1':
        promote = "请输入要查询的system code,可选文件类型,逗号隔开:"
        zq_query(promote)
    elif options.strip() == '2':
        promote = "请输入要下发的system code:"
        sys_id = zq_query(promote)
        zq = input("请输入要下发的账期:")
        release_file(sys_id, zq)
    elif options.strip() == '3':
        sys.exit(1)
    else:
        print("输入有误，请重新输入！ ")


if __name__ == '__main__':
    try:
        execute()
    except Exception as e:
        print(f"出现异常：{e}")
