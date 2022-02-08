import pymysql
import os


def con():
    host = 'jing.tk'
    port = 3312
    username = 'root'
    passwd = 'ROOT#'
    db = 'excel'
    # with pymysql.connect(host=host, port=port, user=username, password=passwd, database=db, charset="utf8") as conn:
    conn = pymysql.connect(host=host, port=port, user=username, password=passwd, database=db, charset="utf8")
    # print(conn)
    conn.select_db("excel")
    cursor = conn.cursor()
    return cursor, conn
    # sql = "select * from table1;"
    # cursor.execute(sql)
    #
    # while 1:
    #     # 每次获取一条数据遍历所有数据
    #     res = cursor.fetchone()
    #     if res is None:
    #         break
    #     print(res)
    #
    # cursor.close()
    # conn.commit()


def close_conn(cur, connect):
    connect.commit
    cur.close
    connect.close


def find_one():
    cursor, conn = con()
    # 查询记录数 同count()函数
    sql = "select * from table1;"
    count = cursor.execute(sql)

    while 1:
        # 每次获取一条数据遍历所有数据
        res = cursor.fetchone()
        if res is None:
            break
        print(res)

    close_conn(cursor, conn)
    # cursor.close()
    # conn.commit()
    # conn.close()
    # 打印总记录数
    print(count)


def find_all():
    cursor, conn = con()
    # 查询记录数 同count()函数
    sql = "select * from log;"
    count = cursor.execute(sql)
    all = cursor.fetchall()
    # print(all)
    for item in all:
        print(item)
    print(count)
    conn.commit()
    cursor.close()
    conn.close()


def find_by_key():
    cursor, conn = con()
    sql = "select * from table1 where id = %s or id = %s;"
    arg = (1, 2)
    count = cursor.execute(sql, arg)
    all = cursor.fetchall()
    print(all)
    print(count)
    close_conn(cursor, conn)


def define_my_sql():
    cursor, conn = con()
    sql = input("please input your sql,eg: select * from xxx;\n")
    cursor.execute(sql)
    all = cursor.fetchall()
    for item in all:
        print(item)
    define_my_sql()


def update_one():
    cursor, conn = con()
    # sql = "insert into log(id,file_name) values (%s,%s);"
    # 主键自增 无需定义主键
    sql = "insert into log(file_name) values (%s);"
    count = -1
    try:
        count = cursor.execute(sql, ('wangwangwang'))
        # a = 1 / 0
        # print(a)
    except Exception as e:
        conn.rollback()
        print(e)
    conn.commit()
    cursor.close()
    conn.close()
    print(count)


def update_many():
    cursor, conn = con()
    sql = "insert into log(id,file_name) values (%s,%s);"
    # 这里元组中的数据不能用单引号
    data = [(2, "lisi"), (3, "wangwu"), (4, "zhaoliu")]
    # 这里使用的executemany
    count = cursor.executemany(sql, data)
    conn.commit()
    cursor.close()
    conn.close()
    # close_conn(cursor, conn)
    print(count)


def find_many_test1():
    cursor, conn = con()
    sql = "select * from table1"
    many = cursor.execute(sql)
    for item in many:
        print(item)


def execute_many_sql():
    cursor, conn = con()

    sql1 = "select * from table1 limit 2"
    cursor.execute(sql1)
    result = cursor.fetchall()
    print(result)
    sql2 = "select * from table1 limit 3"
    cursor.execute(sql2)
    result = cursor.fetchall()
    print(result)
    conn.close()


def query_one_column():
    cursor, conn = con()
    sql = "select id from log"
    cursor.execute(sql)
    res = cursor.fetchall()
    print(res)


if __name__ == '__main__':
    # find_one()
    # find_all()
    # find_by_key()
    # define_my_sql()
    # update_one()
    # update_many()
    # find_many_test1()
    # execute_many_sql()

    try:
        print(111)
        print(1 / 0)
    except Exception as e:
        pass

    print(222)
