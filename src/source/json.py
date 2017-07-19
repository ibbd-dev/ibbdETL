# -*- coding: utf-8 -*-

# Author: mojiehua
# Email: mojh@ibbd.net
# Created Time: 2017-07-19 15:54:58

import json
import requests

class Source:
    """
    从 json 读取数据
    支持的配置参数 params 如下:
    filename: 若从文件中读取 json 数据,则配置成 json 文件路径
    url: 若从 URL 获取 json 数据,则配置成如 http://www.xxx.com/api
    注意: filename 和 url 参数只能选取其中一个进行配置

    encoding: 文件/网页的编码方式,如 utf8 gbk 等
    root: 目标数据支持迭代的 json 根节点,假若目标数据在 json 的一个列表里,如json['weatherinfo']['recent'],此时应设置成 weatherinfo.recent
    fields: 目标字段
    - name: 字段名
      path: 该字段的路径

    - name: 字段名2
      path: 该字段的路径

    配置示例
    source:
      type: json
      params:
        filename: test.json
        encoding: utf8
        root: weatherinfo.recent
        fields:
        - name: day_field
          path: day
        - name: temp_field
          path: temp

      fields:
      - name: day_field
      - name: temp_field
    """

    def __init__(self, params):
        self.url = params['url'] if 'url' in params else None
        self.filename = params['filename'] if 'filename' in params else None
        self.decode = params['encoding'] if 'encoding' in params else None
        self.fields = params['fields']
        self.rootstr = params['root']

    def next(self):
        jsonobj = self.readJson()
        yield from self.parserJson(jsonobj)

    def readJsonByUrl(self,url):
        r = requests.get(url)
        if self.decode:
            r.encoding = self.decode
        else:
            r.encoding = r.apparent_encoding
        return r.json()

    def readJsonByFile(self,path):
        with open(self.filename,'r',encoding=self.decode) as f:
            return json.load(f)

    def readJson(self):
        if self.filename is not None:
            return self.readJsonByFile(self.filename)
        elif self.url is not None:
            return self.readJsonByUrl(self.url)

    def parserJson(self,jsonobj):
        root = jsonobj
        for i in self.rootstr.split('.'):
            root = root[i]

        for item in root:
            row = {}
            for field in self.fields:
                value = item
                for i in field['path'].split('.'):
                    value = value[i]
                row[field['name']] = value
            yield row

    def __del__(self):
        pass

