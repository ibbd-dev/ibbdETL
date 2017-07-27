# -*- coding: utf-8 -*-

# 按某个字段将一行数据分隔成多行数据
# Author: Alex
# Created Time: 2017年05月18日 星期四 10时14分06秒
from copy import deepcopy
import re

class Transform:
    """
    按某个字段将一行数据分隔成多行数据
    配置样例：
    - expand: split
      field: fieldname
      newField: newFieldname
      separator: ','
    注：
    1. field: 原字段。按照某个分隔符扩展成多行之后，原字段会被删除
    2. newField: 新字段，可选，默认和原字段名一样
    3. separator: 分隔符
    """
    config = {}

    def __init__(self, config):
        if 'newField' not in config:
            config['newField'] = config['field']
        self.split_re = re.compile(config['separator'])

        self.config = config

    def do(self, rows):
        config = self.config
        data = []
        for row in rows:
            # tmp = row[config['field']].split(config['separator'])
            tmp = self.split_re.split(row[config['field']])
            if config['field'] != config['newField']:
                del(row[config['field']])

            for i in tmp:
                new_row = deepcopy(row)
                new_row[config['newField']] = i.strip()
                data.append(new_row)

        return data
