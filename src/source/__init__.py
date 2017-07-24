# -*- coding: utf-8 -*-


# 处理source部分配置
# Author: Alex
# Created Time: 2017年05月16日 星期二 10时57分10秒
import re
from importlib import import_module
from src.utils.typeTransform import TypeTransform


class Reader:
    config = {}       # 配置
    source = None     # 数据源操作对象
    match_fields = {}  # 需要处理的字段
    re_match_fields = {}  # 使用正则来匹配字段做处理

    # 字段名映射
    new_keys_list = []
    new_keys_map = {}
    new_keys_init = False

    def __init__(self, config):
        config['fieldNotMatch'] = config['fieldNotMatch'] if 'fieldNotMatch' in config else 'drop'
        if 'fields' in config:
            for field in config['fields']:
                field['trim'] = field['trim'] if 'trim' in field else False
                if 'name' in field:
                    self.match_fields[field['name']] = field
                elif 'fieldMatch' in field:
                    self.re_match_fields[field['fieldMatch']] = field
                else:
                    raise Exception("source的fields属性必须要有name字段或者fieldMatch字段")

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

            # 再做字段处理
            for key in keys:
                if key in self.match_fields:  # 对单个字段做处理
                    row[key] = self._parseField(row[key], self.match_fields[key])
                elif len(self.re_match_fields) > 0:  # 使用正则表达式对多个字段做处理
                    for p in self.re_match_fields:
                        if re.match(p, key) is not None:
                            row[key] = self._parseField(row[key], self.re_match_fields[p])
                            continue
                else:
                    if self.config['fieldNotMatch'] == 'drop':
                        del(row[key])
            yield row


    def _parseField(self, val, config):
        """对单个字段进行处理"""
        if config['trim']:
            val = val.strip()

        if 'defaultValue' in config and val == "":
            return config['defaultValue']

        if 'type' in config:
            return self._parseType(config['type'], val)

        return val

    def _parseType(self, func, val):
        """字段类型转换"""
        return TypeTransform.__dict__[func].__func__(val)

    def _parseNewKeys(self, keys):
        """字段名处理，例如替换特殊字符"""
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

class JoinSourceReader():
    '''
    从两个数据源通过关联读取数据

    配置示例
    source:
      type: csv
      params:
        filename: input.csv
        encoding: gbk
      fields:
      - name: id
      - name: name

    joinSource:
      type: csv
      params:
        filename: joinSource.csv
        encoding: gbk
      fields:
      - name: user_id
      - name: email

      leftField: id
      rightField: user_id

    target:
      type: csv
      params:
        filename: output.csv
    '''
    def __init__(self,config, joinSourceConfig):
        self.joinSourceConfig = joinSourceConfig
        self.reader = Reader(config)
        self.relationMap = self.constructRelationMap(joinSourceConfig)

    def next(self):
        for row in self.reader.next():
            if self.relationMap:
                try:
                    row = dict(row, **self.relationMap[row[self.joinSourceConfig['leftField']]])
                except Exception as e:
                    row = dict(row, **self.relationMap['defaultValue'])
            yield row

    def constructRelationMap(self, joinSourceConfig, defaultValue = None):
        '''
        读取另一个源,以 rightField 作为 key 其他 fields 当做 value
        '''
        relationMap = {}
        reader = Reader(joinSourceConfig)
        for row in reader.next():
            relationMap[row[joinSourceConfig['rightField']]] = row
        for item in relationMap:
            relationMap['defaultValue'] = {key:defaultValue for key in relationMap[item].keys()}
            break
        return relationMap
