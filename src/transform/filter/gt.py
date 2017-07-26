# -*- coding: utf-8 -*-

# Author: mojiehua
# Email: mojh@ibbd.net
# Created Time: 2017-07-26 09:32:53

class Transform:
    """
    某个字段的值大于某个值,则删除该行数据
    field: 字段名
    value: 用来比较的数值
    len: (可选参数)默认值 false 数值比较; 若设置成 true , 则比较字段的长度
    配置样例,该配置表示 age 大于 20 则丢弃该行数据：
    transfrom:
      - type: filter
        name: gt
        field: age
        value: 20
        len: false
    """

    def __init__(self, config):
        self.filed = config['field']
        self.lenMode = config['len'] if 'len' in config else False
        self.value = config['value']
        self.config = config

    def do(self, rows):
        data = []
        for row in rows:
            if self.lenMode:
                if len(str(row[self.filed])) <= self.value:
                    data.append(row)
            elif row[self.filed] <= self.value:
                data.append(row)
        return data
