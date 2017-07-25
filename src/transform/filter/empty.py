# -*- coding: utf-8 -*-

# Author: mojiehua
# Email: mojh@ibbd.net
# Created Time: 2017-07-25 09:45:16

class Transform:
    """
    某个字段的值为空值，则删除该行数据
    field: 字段名
    配置样例：
    transfrom:
      - type: filter
        name: empty
        field: fieldname

    """

    def __init__(self, config):
        self.emptyField = config['field']
        self.config = config

    def do(self, rows):
        data = []
        for row in rows:
            if row[self.emptyField]:
                data.append(row)
        return data
