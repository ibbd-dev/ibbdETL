# -*- coding: utf-8 -*-

# 按模板配置生成新的字符串
# Author: Alex
# Created Time: 2017年05月18日 星期四 10时04分44秒


class Transform:
    """
    按模板配置生成新的字符串
    配置如下:
    - type: modifier
      name: template
      field: fieldname
      template: "hello {fieldname1}, world {fieldname2}"
    注：fieldname1 and fieldname2都是已有的元素，元素的值可以是字符串，整数等。
    """

    def __init__(self):
        pass

    def do(self, rows, config):
        for row in rows:
            row[config['field']] = config['template'].format(**row)

        return rows
