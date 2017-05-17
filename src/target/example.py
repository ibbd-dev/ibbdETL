# -*- coding: utf-8 -*-

# Target样例
# Author: Alex
# Created Time: 2017年05月17日 星期三 17时50分37秒


class Target:
    params = {}

    def __init__(self, params):
        """
        初始化，通常做参数配置
        打开文件操作符等
        """
        self.params = params

    def write(self, row):
        """
        写入单行数据
        """
        pass

    def batch(self, rows):
        """
        批量写入数据
        默认可以不支持批量写入（如果配置了则直接抛异常）
        """
        raise Exception('Not support for batch write')

    def __del__(self):
        """
        退出时可能需要关闭文件操作符等
        """
        pass
