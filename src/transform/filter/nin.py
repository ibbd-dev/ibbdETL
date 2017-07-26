# -*- coding: utf-8 -*-

# Author: mojiehua
# Email: mojh@ibbd.net
# Created Time: 2017-07-26 09:47:03

class Transform:
    """
    某个字段的值不在列表中，则删除该行数据
    field: 字段名
    配置样例：
    transfrom:
      - type: filter
        name: nin
        field: fieldname
        values:
          - value: keepvalue
          - value: keepvalue2
          - value: keepvalue3
    """

    def __init__(self, config):
        self.field = config['field']
        self.values = [i['value'] for i in config['values']]
        self.config = config

    def do(self, rows):
        data = []
        for row in rows:
            if row[self.field] in self.values:
                data.append(row)
        return data
