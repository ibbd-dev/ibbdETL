# -*- coding: utf-8 -*-

# Author: mojiehua
# Email: mojh@ibbd.net
# Created Time: 2017-07-18 14:39:47

import pymysql

class Source:
    params = {}
    reader = None
    def __init__(self, params):
      params['charset'] = params['charset'] if 'charset' in params else 'utf8'
      params['batchNum'] = int(params['batchNum']) if 'batchNum' in params else 1000

      self.params = params
      self.host = params['host']
      self.user = params['user']
      self.passwd = params['passwd']
      self.db = params['db']
      self.charset = params['charset']

    def get_conn(self):
      try:
        conn = pymysql.connect(host = self.host,
                              user = self.user,
                              passwd = self.passwd,
                              db = self.db,
                              charset = self.charset)
        return conn
      except Exception as e:
        print('数据库连接出错',e)
        raise e

    def _query_db(self):
      conn = self.get_conn()
      sql = 'SELECT * from {tb}'.format(tb = self.params['table'])
      cursor = conn.cursor(pymysql.cursors.DictCursor)
      rows_num = cursor.execute(sql)
      for i in range(rows_num//self.params['batchNum'] + 1):
        rows = cursor.fetchmany(self.params['batchNum'])
        for row in rows:
          yield row
      cursor.close()
      conn.close()

    def next(self):
      yield from self._query_db()

    def __del__(self):
        pass
