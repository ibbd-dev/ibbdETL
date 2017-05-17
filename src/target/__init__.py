# -*- coding: utf-8 -*-

# 数据输出对象
# Author: Alex
# Created Time: 2017年05月16日 星期二 10时59分38秒
from copy import deepcopy
from importlib import import_module


class Target:
    """
    数据输出目标对象。配置格式如下
    target:
      type: csv
      batch: false
      batchNum: 10
      params:
        filename: /var/log/test.csv
    """
    config = {}

    # 是否批量写入
    batchWrite = False

    # 每次批量写入的数量
    batchNum = 10

    # 缓存数据，批量写入时需要使用
    rows = []

    def __init__(self, config):
        self.config = config
        if 'batch' in config and config['batch']:  # 批量写入
            self.batchWrite = True
            self.batchNum = config['batchNum']

        if 'params' not in config:
            self.config['params'] = {}

        module = import_module("target." + self.config['type'])
        self.target = module.Target(self.config['params'])

    def write(self, row):
        if self.batchWrite:
            self.rows.append(row)
            if len(self.rows) > self.batchNum:
                rows = deepcopy(self.rows)
                self.rows = []
                self.target.batch(rows)
        else:
            self.target.write(row)

    def __del__(self):
        if len(self.rows) > 0:
            self.target.batch(self.rows)
