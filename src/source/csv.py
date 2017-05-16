# -*- coding: utf-8 -*-

#
# Author: Alex
# Created Time: 2017年05月16日 星期二 11时25分11秒

import csv


class Source:
    params = {}
    reader = {}

    def __init__(self, params):
        self.params = params

        self.csvfile = open(params['filename'], 'r')
        if 'delimiter' not in params:
            params['delimiter'] = ','

        self.reader = csv.DictReader(
            self.csvfile, delimiter=params['delimiter'])

    def nextRow(self):
        for row in self.reader:
            yield row

    def __del__(self):
        self.csvfile.close()
