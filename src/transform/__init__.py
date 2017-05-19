# -*- coding: utf-8 -*-

#
# Author: Alex
# Created Time: 2017年05月16日 星期二 10时58分39秒

from importlib import import_module


class Transform:
    config = {}

    def __init__(self, config):
        self.config = config
        for row in config:
            transform_name = row['type'] + '.' + row['name']
            module = import_module('transform.' + transform_name)
            row['_transform'] = module.Transform(row)

    def do(self, row):
        rows = [row]
        for config in self.config:
            rows = config['_transform'].do(rows)

        for row in rows:
            yield row
