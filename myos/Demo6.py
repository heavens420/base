'''
    数据库链接
'''

import pandas as pd
from sqlalchemy import create_engine

table_name = 'cmp_opt_alarm'
schema = 'gc_cmp'
sql = f"select * from {schema}.{table_name};"


def get_connect():
    engine = create_engine('mysql+pymysql://root:devop#0626@192.168.81.149:3306/gc_cmp')
    res = pd.read_sql_query(sql, engine)
    # print(list(res))
    # print(res.values)
    return list(res), res


def insert_sql():
    data, _ = get_connect()
    sql_str = f"INSERT INTO  {schema}.{table_name}("
    for item in data:
        sql_str += item + ","

    sql_str = sql_str[:-1] + ") VALUES ("
    for i in range(len(data)):
        sql_str += "?,"
    sql_str = sql_str[:-1] + ")"
    print(sql_str)


def update_sql():
    data, _ = get_connect()
    sql_str = f"UPDATE  {schema}.{table_name} set "

    for item in data:
        sql_str += item + "=?,"
    sql_str = sql_str[:-1] + " where id = ?"

    print(sql_str)


def get_data_type():
    _, data = get_connect()
    # print(data.columns)
    # print(data.index)
    # print(data.values)
    # 这是一个 Series 类型
    # print(data.dtypes)
    # 索引 即字段名称
    # print(data.dtypes.index)
    # value 即字段类型
    # print(data.dtypes.values)
    # print(type(data.dtypes))

    columns = data.dtypes.index
    columns_type = data.dtypes.values
    for i in range(len(columns)):
        # print(columns[i] + "---" + str(columns_type[i]))
        pass


def convert_column(col):
    cols = str(col).lower().split("_")
    if len(cols) == 1:
        return cols[0]

    res = cols[0]
    for item in cols[1:]:
        res += item.title()
    return res


def query_sql():
    data, _ = get_connect()
    alias_name_list = table_name.lower().split("_")
    table_alias_name = ''
    for item in alias_name_list:
        table_alias_name += item[0]

    sql_str = 'select \n'
    for col in data:
        column_alias_name = convert_column(col)
        sql_str += "    " + table_alias_name + "." + col + "  " + column_alias_name + ",\n"
    end_sql_from = f"\nfrom {table_name.lower()} {table_alias_name}"
    # end_sql_where = "\n where id = "
    sql_str = sql_str[:-2] + end_sql_from
    print(sql_str)
    return sql_str


if __name__ == '__main__':
    insert_sql()
    print('-' * 100)
    # update_sql()
    # get_data_type()
    # query_sql()
