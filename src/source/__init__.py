# -*- coding: utf-8 -*-


# 处理source部分配置
# Author: Alex
# Created Time: 2017年05月16日 星期二 10时57分10秒

from importlib import import_module


class Reader:
    config = {}
    source = {}

    def __init__(self, config):
        self.config = config

        source_module = import_module("source." + config['type'])
        self.source = source_module.Source(config['params'])

    def nextRow(self):
        for row in self.source.nextRow():
            yield row
