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
    fields: 特殊字段配置
    - name: 检测日期
      config: 字段配置
      - type: date
        format: "yyyy/MM/dd"
    """
    params = {}
    fieldsMap = {}

    # 不同数据类型的配置
    type_config = {
        'integer': {
            'type': 'integer',
        },
        'float': {
            'type': 'float'
        },
        'string': {
            'type': 'string',
            'index': 'not_analyzed'
        }
    }

    is_first = True  # 标注是否为第一行
    mapping = {}   # es mapping的结构

    def __init__(self, params):
        """
        初始化，通常做参数配置
        打开文件操作符等
        """
        self.params = params
        if 'fields' in params:
            for field in params['fields']:
                self.fieldsMap[field['name']] = field['config']

    def write(self, row):
        """
        写入单行数据
        """
        for k in row:
            v = row[k]
            if k in self.fieldsMap:
                self.mapping[k] = self.fieldsMap[k]
            elif type(v) == str:
                new_type = self.parseStr(v)
                if self.is_first:
                    self.mapping[k] = new_type
                else:
                    self.mapping[k] = self.merge(self.mapping[k], new_type)

            else:
                raise Exception("出现了暂时还不支持的数据类型")

        self.is_first = False

    def finish(self):
        with open(self.params['filename'], 'w') as f:
            json.dump({"properties": self.mapping}, f,
                      indent=4, ensure_ascii=False, sort_keys=True)

    def merge(self, old_type, new_type):
        """合并类型"""
        if old_type['type'] == 'string':
            return old_type
        elif new_type['type'] == 'string':
            return new_type
        elif new_type['type'] == 'float' and old_type['type'] == 'integer':
            return new_type

        return old_type

    def parseStr(self, val):
        if re.sub("^\d+$", "", val) == "":
            return self.type_config['integer']
        elif re.sub("^\d+\.\d+$", "", val) == "":
            return self.type_config['float']

        return self.type_config['string']

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
