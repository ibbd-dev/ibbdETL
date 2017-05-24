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
        if 'newField' not in config:
            config['newField'] = config['field']
        self.config = config

    def do(self, rows):
        for row in rows:
            if self.config['useRe']:
                row[self.config['newField']] = re.sub(self.config['old'],
                                                      self.config['new'],
                                                      row[self.config['field']])
            else:
                row[self.config['newField']] = row[self.config['field']].replace(self.config['old'],
                                                                                 self.config['new'])

        return rows
