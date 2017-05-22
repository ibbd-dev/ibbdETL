# -*- coding: utf-8 -*-


# 处理source部分配置
# Author: Alex
# Created Time: 2017年05月16日 星期二 10时57分10秒

from importlib import import_module
from utils.typeTransform import TypeTransform


class Reader:
    config = {}
    source = {}
    match_fields = {}

    def __init__(self, config):
        if 'fields' in config:
            if 'fieldNotMatch' not in config:
                config['fieldNotMatch'] = 'drop'
            for field in config['fields']:
                if 'trim' not in field:
                    field['trim'] = False
                self.match_fields[field['name']] = field

        self.config = config
        module = import_module("source." + config['type'])
        self.source = module.Source(config['params'])

    def next(self):
        for row in self.source.next():
            keys = list(row.keys())
            for key in keys:
                if key in self.match_fields:
                    if 'type' in self.match_fields[key]:
                        row[key] = self._parseType(self.match_fields[key]['type'],
                                                   row[key])
                    if 'defaultValue' in self.match_fields[key] \
                            and row[key] == "":
                        row[key] = self.match_fields[key]['defaultValue']
                    if self.match_fields[key]['trim']:
                        row[key] = row[key].strip()
                else:
                    if self.config['fieldNotMatch'] == 'drop':
                        del(row[key])

            yield row

    def _parseType(self, func, val):
        return TypeTransform.__dict__[func].__func__(val)
