# -*- coding: utf-8 -*-


# 处理source部分配置
# Author: Alex
# Created Time: 2017年05月16日 星期二 10时57分10秒

from importlib import import_module
from src.utils.typeTransform import TypeTransform


class Reader:
    config = {}       # 配置
    source = None     # 数据源操作对象
    match_fields = {}  # 需要处理的字段

    # 字段名映射
    new_keys_list = []
    new_keys_map = {}
    new_keys_init = False

    def __init__(self, config):
        if 'fields' in config:
            if 'fieldNotMatch' not in config:
                config['fieldNotMatch'] = 'drop'
            for field in config['fields']:
                if 'trim' not in field:
                    field['trim'] = False
                self.match_fields[field['name']] = field

        self.config = config
        module = import_module("src.source." + config['type'])
        self.source = module.Source(config['params'])

    def next(self):
        for row in self.source.next():
            keys = list(row.keys())
            if not self.new_keys_init:
                self._parseNewKeys(keys)
                self.new_keys_init = True

            # 先做字段名的映射
            if len(self.new_keys_map) > 0:
                new_row = {}
                for key in keys:
                    new_row[self.new_keys_map[key]] = row[key]
                row = new_row
                keys = self.new_keys_list

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

    def _parseNewKeys(self, keys):
        if 'fieldsNameMap' not in self.config:
            return

        for conf in self.config['fieldsNameMap']:
            if conf['name'] == 'replace':
                for key in keys:
                    new_key = key.replace(conf['old'], conf['new'])
                    new_key = new_key.strip()
                    self.new_keys_list.append(new_key)
                    self.new_keys_map[key] = new_key
        return
