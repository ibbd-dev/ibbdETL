# -*- coding: utf-8 -*-

# Author: mojiehua
# Email: mojh@ibbd.net
# Created Time: 2017-07-20 09:35:24

import json

class Target:
    """
    写入 json 文件
    支持的配置参数 params 如下:
    filename: 文件名
    encoding: 文件编码方式,默认以 utf8 编码

    配置示例
    target:
      params:
        filename: jsonoutput.json
    """
    def __init__(self, params):
        self.filename = params['filename']
        self.encoding = params['encoding'] if 'encoding' in params else 'utf8'
        self.json_buffer = []


    def write(self, row):
        self.json_buffer.append(row)


    def batch(self, rows):
        for row in rows:
            self.json_buffer.append(row)

    def __del__(self):
        with open(self.filename,'w',encoding=self.encoding) as f:
            json.dump(self.json_buffer, f, ensure_ascii=False)
