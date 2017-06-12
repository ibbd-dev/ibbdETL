# -*- coding: utf-8 -*-

#
# Author: Alex
# Created Time: 2017年05月16日 星期二 10时58分39秒
from copy import deepcopy
from importlib import import_module


class Transform:
    config = {}

    def __init__(self, config):
        for row in config:
            transform_name = row['type'] + '.' + row['name']
            module = import_module('src.transform.' + transform_name)
            row['_transform'] = module.Transform(row)

            if 'log' not in row:
                row['log'] = False
            elif type(row['log']) != bool:
                raise Exception("log type is not bool in %s" % transform_name)

        self.config = config

    def do(self, row):
        rows = [row]
        _rows = rows
        for conf in self.config:
            if conf['log']:
                _rows = deepcopy(rows)   # 保存原有的数据

            rows = conf['_transform'].do(rows)
            if conf['log'] and rows != _rows:
                print("%s: %s =>" % (conf['type'], conf['name']))
                print(rows)
                print(_rows)

        for row in rows:
            yield row
