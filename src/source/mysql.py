# -*- coding: utf-8 -*-

# Author: mojiehua
# Email: mojh@ibbd.net
# Created Time: 2017-07-18 14:39:47

import pymysql

class Source:
    """
    从 MySQL 数据库读取数据
    支持的配置参数 params 如下:
    host: MySQL 主机地址
    port: MySQL 端口(可选参数,默认3306)
    user: 用户名
    passwd: 密码
    db: 数据库
    table: 表名
    charset: 字符集(可选参数,默认设置成UTF8)
    batchNum: 批量从数据库读取数据,默认每1000条来读取
    fields: 需要读取的列名,默认SELECT * FROM table

    配置示例
    params:
      host: 127.0.0.1
      port: 3306
      user: root
      passwd: root
      db: test
      charset: utf8
      table: testmysql
      batchNum: 1000
      fields:
        - id
        - name
        - email
        - age
    """

    def __init__(self, params):
        params['charset'] = params['charset'] if 'charset' in params else 'utf8'
        params['port'] = int(params['port']) if 'port' in params else 3306
        params['batchNum'] = int(params['batchNum']) if 'batchNum' in params else 1000

        self.params = params
        self._host = params['host']
        self._port = params['port']
        self._user = params['user']
        self._passwd = params['passwd']
        self._db = params['db']
        self._charset = params['charset']

    def next(self):
        yield from self._query_db()

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

    def _query_db(self):
        conn = self.get_conn()
        sql = ''
        if 'fields' not in self.params:
            sql = 'SELECT * from {tb}'.format(tb = self.params['table'])
        else:
            sql = 'SELECT {cloumns} FROM {tb}'.format(cloumns=','.join(self.params['fields']), tb=self.params['table'])
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        rows_num = cursor.execute(sql)
        for i in range(rows_num//self.params['batchNum'] + 1):
            rows = cursor.fetchmany(self.params['batchNum'])
            for row in rows:
                yield row
        cursor.close()
        conn.close()

    def __del__(self):
        pass
