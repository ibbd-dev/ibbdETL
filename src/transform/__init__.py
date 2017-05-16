# -*- coding: utf-8 -*-

#
# Author: Alex
# Created Time: 2017年05月16日 星期二 10时58分39秒

from importlib import import_module


class Transform:
    config = {}
    obj = {}

    def __init__(self, config):
        self.config = config
        for row in config:
            obj_name = row['type'] + '.' + row['name']
            if obj_name not in self.obj:
                module = import_module('transform.' + obj_name)
                self.obj[obj_name] = module.Transform()

    def do(self, row):
        rows = [row]
        for config in self.config:
            obj_name = config['type'] + '.' + config['name']
            rows = self.obj[obj_name].do(rows, config)

        for row in rows:
            yield row
