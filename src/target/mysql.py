# -*- coding: utf-8 -*-

# Author: mojiehua
# Email: mojh@ibbd.net
# Created Time: 2017-07-18 17:38:44

import pymysql

class Target:
    """
    写入 MySQL 数据库,需要预先创建表,字段应与输出的字段一致
    支持的配置参数 params 如下:
    host: MySQL 主机地址
    port: MySQL 端口(可选参数,默认3306)
    user: 用户名
    passwd: 密码
    db: 数据库
    table: 表名
    charset: 字符集(可选参数,默认设置成UTF8)

    配置示例
    params:
        host: 127.0.0.1
        port: 3306
        user: root
        passwd: root
        db: test
        charset: utf8
        table: testmysql
        batch: true
        batchNum: 1000
    """
    params = {}

    def __init__(self, params):
        params['charset'] = params['charset'] if 'charset' in params else 'utf8'
        params['port'] = int(params['port']) if 'port' in params else 3306

        self.params = params
        self._host = params['host']
        self._port = params['port']
        self._user = params['user']
        self._passwd = params['passwd']
        self._db = params['db']
        self._charset = params['charset']
        self._table = params['table']
        self._conn = None
        self._cursor = None

    def get_conn(self):
        try:
            conn = pymysql.connect(host = self._host,
                                  port = self._port,
                                  user = self._user,
                                  passwd = self._passwd,
                                  db = self._db,
                                  charset = self._charset)
            return conn
        except Exception as e:
            print('数据库连接出错',e)
            raise e

    def write(self, row):
        if self._conn is None:
            self._conn = self.get_conn()
            self._cursor = self._conn.cursor()
        sql = self.constructSQLByRow(row)
        try:
            self._cursor.execute(sql,(list(row.values())))
            self._conn.commit()
        except Exception as e:
            print(e)
            print('插入数据库出错,忽略此条记录',row)

    def constructSQLByRow(self,row):
        fields = ','.join(row.keys())
        values = ','.join(['%s' for _ in row.values()])
        sql = '''INSERT INTO {tb}({column}) VALUES ({values}) '''.format(tb=self._table,column=fields,values=values)
        return sql

    def batch(self, rows):
        if self._conn is None:
            self._conn = self.get_conn()
            self._cursor = self._conn.cursor()
        for row in rows:
            try:
                sql = self.constructSQLByRow(row)
                self._cursor.execute(sql,(list(row.values())))
            except Exception as e:
                print(e)
                print('插入数据库出错,忽略此条记录',row)
        self._conn.commit()

    def __del__(self):
        if self._cursor:
            self._cursor.close()
        if self._conn:
            self._conn.close()
