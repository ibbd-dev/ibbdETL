# -*- coding: utf-8 -*-

# Author: mojiehua
# Email: mojh@ibbd.net
# Created Time: 2017-07-25 09:49:47

class Transform:
    """
    某个字段的值等于某个值,则删除该行数据(转换成字符串进行比较)
    field: 字段名
    配置样例：
    transfrom:
      - type: filter
        name: eq
        field: fieldname
        value: somevalue
    """

    def __init__(self, config):
        self.eqField = config['field']
        self.value = str(config['value'])
        self.config = config

    def do(self, rows):
        data = []
        for row in rows:
            if str(row[self.eqField]) == self.value:
                continue
            else:
                data.append(row)
        return data
