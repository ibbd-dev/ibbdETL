# -*- coding: utf-8 -*-

# 将数据写入csv文件
# Author: Alex
# Created Time: 2017年05月17日 星期三 16时18分34秒

import csv


class Target:
    params = {}
    writer = False

    def __init__(self, params):
        self.params = params

        self.csvfile = open(params['filename'], 'w')
        if 'delimiter' not in params:
            self.params['delimiter'] = ','

    def write(self, row):
        if not self.writer:
            fieldnames = list(row.keys())
            self.writer = csv.DictWriter(self.csvfile, fieldnames=fieldnames)
            self.writer.writeheader()
        self.writer.writerow(row)

    def batch(self, rows):
        if not self.writer:
            fieldnames = list(rows[0].keys())
            self.writer = csv.DictWriter(self.csvfile, fieldnames=fieldnames)
            self.writer.writeheader()

        for row in rows:
            self.writer.writerow(row)


    def __del__(self):
        self.csvfile.close()
