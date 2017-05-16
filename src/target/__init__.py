# -*- coding: utf-8 -*-

#
# Author: Alex
# Created Time: 2017年05月16日 星期二 10时59分38秒


class Target:
    config = {}

    def __init__(self, config):
        self.config = config

    def write(self, row):
        print("\t".join(row))
