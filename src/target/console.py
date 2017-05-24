# -*- coding: utf-8 -*-

# 数据输出到控制台
# Author: Alex
# Created Time: 2017年05月17日 星期三 17时50分37秒


class Target:
    params = {}

    def __init__(self, params):
        self.params = params

        if 'delimiter' not in params:
            self.params['delimiter'] = "\t"   # 默认分隔符

    def write(self, row):
        if type(row) == dict:
            print(row)
        else:
            print(self.params['delimiter'].join(row))

    def batch(self, rows):
        for row in rows:
            self.write(row)

    def flush(self):
        pass
