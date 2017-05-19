# -*- coding: utf-8 -*-

# 数据类型转换
# Author: Alex
# Created Time: 2017年05月18日 星期四 10时04分44秒
from utils.typeTransform import TypeTransform


class Transform:
    """
    数据类型转换
    配置如下:
    - type: modifier
      name: typeTransform
      field: age
      newType: int
    """
    config = {}

    def __init__(self, config):
        self.config = config

    def do(self, rows):
        for row in rows:
            row[self.config['field']] = self._parseType(self.config['newType'],
                                                        row[self.config['field']])

        return rows

    def _parseType(self, func, val):
        return TypeTransform.__dict__[func].__func__(val)
