# -*- coding: utf-8 -*-

# ElasticSearch数据写入
# Author: Alex
# Created Time: 2017年05月22日 星期一 11时37分00秒
from database.elasticsearch import IbbdElasticSearch


class Target:
    es = None
    params = {}

    def __init__(self, params):
        """
        初始化，通常做参数配置
        打开文件操作符等
        """
        self.es = IbbdElasticSearch(params)
        self.params = params

    def write(self, row):
        """
        写入单行数据
        """
        self.es.write(row)

    def batch(self, rows):
        """
        批量写入数据
        默认可以不支持批量写入（如果配置了则直接抛异常）
        """
        self.es.batchWrite(rows)

    def __del__(self):
        """
        退出时可能需要关闭文件操作符等
        """
        pass
