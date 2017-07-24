# -*- coding: utf-8 -*-

# Author: mojiehua
# Email: mojh@ibbd.net
# Created Time: 2017-07-24 11:20:54

class Transform:
    """
    按某个字段设置唯一属性
    field: 设置唯一值的字段名
    配置样例：
    transfrom:
      - type: filter
        name: unique
        field: fieldname

    """
    config = {}

    def __init__(self, config):
        self.uniqueField = config['field'] if 'field' in config else None
        self.config = config
        self.unique = set()

    def do(self, rows):
        data = []
        if self.uniqueField is None:
            return rows
        for row in rows:
            if row[self.uniqueField] in self.unique:
                continue
            else:
                data.append(row)
                self.unique.add(row[self.uniqueField])
        return data
