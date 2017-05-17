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

    def nextRow(self):
        for row in self.source.nextRow():
            if 'fields' in self.config:
                for field in self.config['fields']:
                    row[field['name']] = self._parseType(field['type'],
                                                         row[field['name']])

            yield row

    def _parseType(self, func, val):
        return TypeTransform.__dict__[func].__func__(val)
