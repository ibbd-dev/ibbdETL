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

    def __init__(self):
        pass

    def do(self, rows, config):
        for row in rows:
            row[config['field']] = self._parseType(config['newType'],
                                                   row[config['field']])

        return rows

    def _parseType(self, func, val):
        return TypeTransform.__dict__[func].__func__(val)
