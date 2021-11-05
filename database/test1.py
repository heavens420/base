import pymysql

'''
    数据检索模块，支持自定义sql查询(可关联查询)和单表的任意单字段查询
'''


class Search:
    def __init__(self):
        self.__host = 'jing.tk'
        self.__port = 3312
        self.__username = 'root'
        self.__passwd = 'ROOT#'
        self.__db = 'excel'
        self.table_name = ''

    # 创建数据库连接
    def __con(self):
        conn = pymysql.connect(host=self.__host,
                               port=self.__port,
                               user=self.__username,
                               password=self.__passwd,
                               database=self.__db,
                               charset="utf8")
        # 选择操作的数据库
        conn.select_db("excel")
        # 获取游标，参数的含义是使查询结果返回为json格式
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # cursor = conn.cursor()
        return cursor, conn

    # 执行条件查询
    def exec_find_by_key(self, search_type):
        # 获取数据库连接
        cursor, conn = self.__con()
        # 打印可选数据表
        self.table_list()
        # 打印表字段
        self.table_title(search_type)
        # 执行条件查询
        self.find_by_key(cursor, conn, self.table_name)

    # 按条件查询实现
    def find_by_key(self, cursor, conn, table):
        try:
            # 输入查询的条件 key,value 形式 如果输入quit则正常退出当前程序
            in_param = str(input("请输入要查的字段名称和字段值，空格分隔，如：id 2=>"))
            # 结束程序
            if in_param == 'quit' or in_param == 'exit':
                cursor.close()
                conn.close()
                return ''

            # 参数转换获取key value
            key, value = in_param.split(" ")
            key = str(key).strip().lower()
            value = str(value).strip().lower()

            # 执行的sql语句
            sql = f"select * from {table} where {key} = {value}"
            # 执行查询操作
            cursor.execute(sql)
        except Exception as e:
            print(f"查询失败:{e}")
            # 发生异常 则递归调用方法 不退出当前方法
            self.find_by_key(cursor, conn, table)
        # 执行查询语句
        result = cursor.fetchall()
        # 打印执行结果
        for item in result:
            print(item)
        # 提交事务
        conn.commit()
        # cursor.close()
        # conn.close()
        # 递归调用当前方法 可二次执行查询
        self.find_by_key(cursor, conn, table)

    # 执行自定义sql
    def exec_define_sql(self, search_type):
        # 获取数据库连接
        cursor, conn = self.__con()
        # 打印可操作的数据表
        self.table_list()
        # 打印数据表字段信息
        self.table_title(search_type)
        # 执行自定义sql操作
        self.define_sql(cursor, conn)

    # 实现自定义sql操作
    def define_sql(self, cursor, conn):
        # 要执行的sql语句
        sql = str(input("请输入自定义sql(输入quit退出)=>"))
        # 退出条件
        key = str(sql).strip().lower()
        if key == 'quit' or key == 'exit':
            # 关闭数据库连接 和游标
            cursor.close()
            conn.close()
            return

        try:
            # 执行sql
            cursor.execute(sql)
        except Exception as e:
            print(f"sql有误:{e}")
            # 出现异常 递归执行当前方法 避免直接退出程序
            self.define_sql(cursor, conn)
        # 获取执行结果
        result = cursor.fetchall()
        # 遍历打印执行结果
        for item in result:
            print(item)
        # 提交事务
        conn.commit()
        # 递归执行 可二次执行自定义sql操作
        self.define_sql(cursor, conn)

    # 打印表格字段信息
    def table_title(self, search_type):
        # t_sys表字段信息
        t_sys_list = [{'字段名': '字段描述'}, {'id': '自增主键'}, {'sys_name': '系统名称'}, {'back_type': '备份方式'},
                      {'back_cycle': '备份周期'},
                      {'duration': '保存时长'}]
        # t_back_log表字段信息
        t_back_log_list = [{'字段名': '字段描述'}, {'id': '自增主键'}, {'sys_name': '系统名称'}, {'back_cycle': '备份周期'},
                           {'back_date': '备份时间'}, {'file_size': '文件大小'},
                           {'collect_date': '采集时间'}, {'finish_date': '采集完成时间'}, {'file_num': '备份文件数量'},
                           {'check_failed_num': '校验失败数量'}, {'status_cd': '文件是否过期'}]
        # 要打印的表字段信息
        target_list = []
        # 不同功能的不同提示语
        if search_type == '1' or search_type == '':
            # 为1 或者直接回车情况
            search_type = '1'
            table = str(input("请输入要查看的表名(输入回车跳过此步骤)=>"))
        else:
            # 其它情况
            table = str(input("请输入要查询的表名=>"))

        # 不输入表名 不打印表名
        if table.strip() == '':
            pass
        else:
            # 输入表名 打印表名并保存表名给其它函数使用
            self.table_name = table
            print(f"您输入的表名为:{table}")

        # 输入不同表名 打印不同表信息
        if table == 't_sys':
            target_list = t_sys_list
        elif table == 't_back_log':
            target_list = t_back_log_list
        # 未输入表名
        elif table == '':
            # 且选择的不是自定义sql功能
            if search_type != '1':
                # 则要求重新输入表名
                self.table_title(search_type)
        else:
            # 输入的表名不存在或无查询权限 要求重新输入
            print("表名输入有误，请重新输入")
            self.table_title(search_type)
        # 打印表字段信息
        self.for_dict(target_list)

    # 可查看或查询的表名列表
    def table_list(self):
        lst = [{'表名': '描述'}, {'t_sys': '系统清单表'}, {'t_back_log': '备份记录表'}, {'t_release': '数据下发表'}]
        self.for_dict(lst)

    # 打印字典值
    def for_dict(self, lst):
        for item in lst:
            for key in item:
                print(key + " : " + item[key] + "\t")

    # 功能执行选择入口
    def exec_sql(self):
        # 可执行的功能代号
        search_type = str(input("请输入以下序号，默认为1\n1：自定义sql查询\n2：输入参数单表查询\n"))
        if search_type == '1' or search_type.strip() == '':
            print(f"您选择的是1：自定义sql查询")
            self.exec_define_sql(search_type)
        elif search_type == '2':
            print("您选择的是2：输入参数单表查询")
            self.exec_find_by_key(search_type)
        else:
            # raise Exception("输入有误，请重新输入")
            print("输入有误，请重新输入")
            self.exec_sql()


if __name__ == '__main__':
    p = Search()
    try:
        p.exec_sql()
    except Exception as e:
        print(f"异常：{e}")
