# -*- coding: utf-8 -*-

# 对某个字段做hash运算，并保存为新的字段
# Author: Alex
# Created Time: 2017年05月16日 星期二 16时45分04秒

import hashlib


class Transform:
    """
    对某个字段做hash运算，并保存为新的字段
    - type: modifier
      name: hash
      field: name
      newField: name_hash
    """
    config = {}

    def __init__(self, config):
        if 'len' not in config:
            config['len'] = 10
        self.config = config

    def do(self, rows):
        config = self.config

        for row in rows:
            if len(row[config['field']]) > 0:
                row[config['newField']] = self._hash(row[config['field']],
                                                     config['len'])
            else:
                row[config['newField']] = ''

        return rows

    def _hash(self, val, hash_len):
        return hashlib.sha1(bytes(val, encoding="utf-8")).hexdigest()[0:hash_len]
