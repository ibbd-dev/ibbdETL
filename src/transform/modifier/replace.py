# -*- coding: utf-8 -*-
# 字符串替换
# Author: Alex
# Created Time: 2017年05月24日 星期三 15时57分13秒
import re


class Transform:
    """
    按模板配置生成新的字符串
    配置如下:
    - type: modifier
      name: replace
      field: fieldname
      newField: new_fieldname
      useRe: false
      old: ""
      new: ""
    注：old和new可以支持正则匹配，具体有参数useRe决定（默认不使用正则）
    new_fieldname: 该参数可选，默认与field参数一致
    """
    config = {}

    def __init__(self, config):
        if 'useRe' not in config:
            config['useRe'] = False

        if config['useRe']:
            config['old'] = re.compile(config['config'])

        if 'newField' not in config:
            config['newField'] = config['field']

        self.config = config

    def do(self, rows):
        replace = self._replace
        if self.config['useRe']:
            replace = self._re_replace

        for row in rows:
            row[self.config['newField']] = replace(row[self.config['field']])

        return rows

    def _re_replace(self, val):
        return re.config['old'].sub(self.config['new'], val)

    def _replace(self, val):
        return val.replace(self.config['old'],
                           self.config['new'])

