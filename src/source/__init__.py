# -*- coding: utf-8 -*-


# 处理source部分配置
# Author: Alex
# Created Time: 2017年05月16日 星期二 10时57分10秒

from importlib import import_module
from utils.typeTransform import TypeTransform


class Reader:
    config = {}
    source = {}

    def __init__(self, config):
        self.config = config

        module = import_module("source." + config['type'])
        self.source = module.Source(config['params'])

    def next(self):
        for row in self.source.next():
            res = {}
            for field in self.config['fields']:
                if 'type' not in field:
                    res[field['name']] = row[field['name']]
                else:
                    res[field['name']] = self._parseType(field['type'],
                                                         row[field['name']])

            yield res

    def _parseType(self, func, val):
        return TypeTransform.__dict__[func].__func__(val)
