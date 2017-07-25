# -*- coding: utf-8 -*-

# Author: mojiehua
# Email: mojh@ibbd.net
# Created Time: 2017-07-25 09:54:35

class Transform:
    """
    某个字段的值在列表中，则删除该行数据
    field: 字段名
    配置样例：
    transfrom:
      - type: filter
        name: in
        field: fieldname
        values:
          - dropvalue
          - dropvalue2
          - dorpvalue3
    """

    def __init__(self, config):
        self.field = config['field']
        self.values = list(map(str,config['values']))
        self.config = config

    def do(self, rows):
        data = []
        for row in rows:
            if str(row[self.field]) in self.values:
                continue
            else:
                data.append(row)
        return data
