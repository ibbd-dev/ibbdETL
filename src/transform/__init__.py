# -*- coding: utf-8 -*-

#
# Author: Alex
# Created Time: 2017年05月16日 星期二 10时58分39秒

import imp
from copy import deepcopy
from importlib import import_module


class Transform:
    config = {}

    def __init__(self, config):
        for each_config in config:
            if 'user' == each_config['type']:
                module = imp.load_source('Transform', config['path'])
                each_config['transformFunc'] = getattr(module, config['func'])
            else:
                module = import_module('src.transform.' + each_config['type'] + '.' + each_config['name'])
                each_config['transformFunc'] = module.Transform(each_config).do

            if 'log' not in each_config:
                each_config['log'] = False
            elif type(each_config['log']) != bool:
                raise Exception("log type is not bool in ",each_config)

        self.config = config

    def do(self, row):
        rows = [row]
        _rows = rows
        for conf in self.config:
            if conf['log']:
                _rows = deepcopy(rows)   # 保存原有的数据

            rows = conf['transformFunc'](rows)
            if conf['log'] and rows != _rows:
                print("%s: %s =>" % (conf['type'], conf['name']))
                print(rows)
                print(_rows)

        for row in rows:
            yield row
