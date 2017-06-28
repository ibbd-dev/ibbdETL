# -*- coding: utf-8 -*-

# 给某个字段增加前缀
# Author: Alex
# Created Time: 2017年05月16日 星期二 16时45分04秒


class Transform:
    """
    给某个字段增加前缀
    - type: modifier
      name: addPrefix
      field: fieldname
      prefix: 'u.'
    """
    config = {}

    def __init__(self, config):
        self.config = config

    def do(self, rows):
        config = self.config
        for row in rows:
            if len(row[config['field']]) > 0:
                row[config['field']] = config['prefix'] + row[config['field']]
            else:
                row[config['field']] = ''
        return rows
