# -*- coding: utf-8 -*-

#
# Author: Alex
# Created Time: 2017年05月16日 星期二 11时25分11秒

import os
import csv
import codecs

class Source:
    params = {}
    reader = None

    def __init__(self, params):
        if 'encoding' not in params:
            params['encoding'] = 'utf-8'
        self.params = params

        if not os.path.isfile(params['filename']):
            raise Exception('%s 文件不存在' % params['filename'])

        self.csvfile = open(params['filename'], 'r', encoding=params['encoding'])
        if 'delimiter' not in params:
            params['delimiter'] = ','

        self.reader = csv.DictReader(
            self.csvfile, delimiter=params['delimiter'])

    def next(self):
        for row in self.reader:
            yield row

    def __del__(self):
        self.csvfile.close()
