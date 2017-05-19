# -*- coding: utf-8 -*-

# 将值一一映射为相应的值
# Author: Alex
# Created Time: 2017年05月18日 星期三 15时04分51秒


class Transform:
    """
    将值一一映射为相应的值
    从fromFieldName字段映射到toFieldName字段
    配置如下:
    - type: modifier
      name: mapping
      from: fromFieldName
      to: toFieldName
      default: 0
      mapping:
      - from: '第一期'
        to: 1
      - from: '第二期'
        to: 2
      - from: '第三期'
        to: 3
    """
    config = {}
    mappings = {}

    def __init__(self, config):
        for m in config['mapping']:
            self.mappings[m['from']] = m['to']

        self.config = config

    def do(self, rows):
        config = self.config
        fromField = config['from']
        toField = config['to']
        for row in rows:
            if row[fromField] in self.mappings:
                row[toField] = self.mappings[row[fromField]]
            else:
                row[toField] = config['default']
        return rows


if __name__ == '__main__':
    config = {
        'type': 'modifier',
        'name': 'mapping',
        'from': 'fromField',
        'to': 'toField',
        'default': 0,
        'mapping': [
            {'from': '第一期', 'to': 1},
            {'from': '第二期', 'to': 2},
            {'from': '第三期', 'to': 3},
        ]
    }

    rows = [
        {'fromField': '第一期', 'hello': 10},
        {'fromField': '第二期', 'hello': 10},
        {'fromField': '第四期', 'hello': 10},
        {'fromField': '第五期', 'hello': 10},
    ]

    tsf = Transform(config)
    print(tsf.do(rows))
