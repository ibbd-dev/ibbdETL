# -*- coding: utf-8 -*-

# 类型转换
# Author: Alex
# Created Time: 2017年05月17日 星期三 15时56分53秒


class TypeTransform:

    @staticmethod
    def float(val):
        return float(val)

    @staticmethod
    def int(val):
        return int(val)

    @staticmethod
    def str(val):
        return str(val)

    @staticmethod
    def date(val):
        """
        格式化日期
        """
        tmp = val.split('-')
        return "%s-%02d-%02d" % (tmp[0], int(tmp[1]), int(tmp[2]))
