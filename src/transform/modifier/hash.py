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

    def __init__(self):
        pass

    def do(self, rows, config):
        if 'len' not in config:
            config['len'] = 10

        for row in rows:
            if len(row[config['field']]) > 0:
                row[config['newField']] = self._hash(row[config['field']],
                                                     config['len'])
            else:
                row[config['newField']] = ''

        return rows

    def _hash(self, val, hash_len):
        return hashlib.sha1(bytes(val, encoding="utf-8")).hexdigest()[0:hash_len]
