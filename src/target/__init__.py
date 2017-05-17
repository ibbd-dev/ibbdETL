# -*- coding: utf-8 -*-

#
# Author: Alex
# Created Time: 2017年05月16日 星期二 10时59分38秒
from importlib import import_module


class Target:
    config = {}

    def __init__(self, config):
        self.config = config

        module = import_module("target." + config['type'])
        self.target = module.Target(config['params'])

    def write(self, row):
        self.target.write(row)
