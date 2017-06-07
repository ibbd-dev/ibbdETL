# -*- coding: utf-8 -*-

# 输出为esMapping的配置文件（json格式）
# Author: Alex
# Created Time: 2017年06月07日 星期三 11时18分08秒
import re
import json


class Target:
    """
    写入es的mapping配置文件。支持参数：
    filename: 文件名
    """
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
        data = {}
        for k in row:
            v = row[k]
            if type(v) == str:
                data[k] = self.parseStr(v)
            else:
                raise Exception("出现了暂时还不支持的数据类型")

        with open(self.params['filename'], 'w') as f:
            json.dump({"properties": data}, f, indent=4, ensure_ascii=False)

    def parseStr(self, val):
        if re.sub("^\d+$", "", val) == "":
            return {
                'type': 'integer'
            }
        elif re.sub("^\d+\.\d+$", "", val) == "":
            return {
                'type': 'float'
            }
        return {
            'type': 'string',
            'index': 'not_analyzed'
        }

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
