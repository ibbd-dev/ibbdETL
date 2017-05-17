# -*- coding: utf-8 -*-

# 经纬度坐标转换
# 用于百度坐标系(bd-09)、火星坐标系(国测局坐标系、gcj02)、WGS84坐标系的相互转换
# Author: Alex
# Created Time: 2017年05月17日 星期三 15时04分51秒

from utils.coordTransform import CoordTransform


class Transform:
    """
    经纬度坐标转换，支持以下坐标:
        bd09: 百度坐标系
        gcj02: 火星坐标系（国标）。中国标准，从国行移动设备中定位获取的坐标数据使用这个坐标系
        wgs84: 国际标准，从 GPS 设备中取出的数据的坐标系
    配置如下:
        - type: modifier
          name: coordTransform
          from:
            type: wgs84
            lngField: lng
            latField: lat
          to:
            type: bd09
            latField: lat
            lngField: lng
    """

    def __init__(self):
        pass

    def do(self, rows, config):
        func_name = "%s_to_%s" % (config['from']['type'], config['to']['type'])
        for row in rows:
            lng, lat = self._parse(row[config['from']['lngField']],
                                   row[config['from']['latField']],
                                   func_name)
            row[config['to']['lngField']], row[config['to']['latField']] = lng, lat

        return rows

    def _parse(self, lng, lat, func_name):
        return CoordTransform.__dict__[func_name].__func__(lng, lat)
