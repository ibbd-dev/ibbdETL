# -*- coding: utf-8 -*-

# 符号运算
# Author: Alex
# Created Time: 2017年05月18日 星期四 10时04分44秒


class Transform:
    """
    符号运算
    先用模板生成相应的字符串，然后计算
    配置如下:
    - type: modifier
      name: symbolic
      field: fieldname
      template: "{fieldname1} * 2 + 3"
    注：fieldname1是一个字段名
    """

    def __init__(self):
        pass

    def do(self, rows, config):
        for row in rows:
            row[config['field']] = eval(config['template'].format(**row))

        return rows
