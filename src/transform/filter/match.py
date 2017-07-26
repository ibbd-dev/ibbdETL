# -*- coding: utf-8 -*-

# Author: mojiehua
# Email: mojh@ibbd.net
# Created Time: 2017-07-26 09:52:54

import re

class Transform:
    """
    某个字段的值满足某正则表达式的，则执行 action 操作,默认 drop 删除
    field: 字段名
    action: 可以设置成 keep 或 drop
            设置成 keep 表示满足正则的都保留，不满足的都删除
            设置成 drop 表示满足正则的都删除，不满足的都保留
    配置样例：
    transfrom:
      - type: filter
        name: match
        field: name
        pattern: ^[张]
        action: drop
    """

    def __init__(self, config):
        self.field = config['field']
        self.rePattern = re.compile(config['pattern'])
        self.drop = {'drop':True,'keep':False}[config['action']] if 'action' in config else True
        self.keep = not self.drop
        self.config = config

    def do(self, rows):
        data = []
        for row in rows:
            matchResult = re.match(self.rePattern,row[self.field])
            if self.keep and matchResult:
                data.append(row)
            elif self.drop and (not matchResult):
                data.append(row)
        return data
