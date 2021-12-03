import datetime
import os
import pymysql

'''
    发送周报月报 报告备份信息
'''


def con():
    host = 'jing.tk'
    port = 3313
    username = 'root'
    passwd = 'ROOT#'
    db = 'data_back'
    # with pymysql.connect(host=host, port=port, user=username, password=passwd, database=db, charset="utf8") as conn:
    conn = pymysql.connect(host=host, port=port, user=username, password=passwd, database=db, charset="utf8")
    # print(conn)
    conn.select_db("data_back")
    cursor = conn.cursor()
    return cursor, conn


def send_week_report():
    cursor, conn = con()
    sql = f"select "