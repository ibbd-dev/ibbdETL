# -*- coding: utf-8 -*-

# elasticsearch
# Author: Alex
# Created Time: 2017年05月22日 星期一 10时00分04秒
import json
from pyelasticsearch import ElasticSearch
from pyelasticsearch import ElasticHttpNotFoundError


class IbbdElasticSearch:
    """
    es操作
    文档：http://pyelasticsearch.readthedocs.io/en/latest/
    """
    es = None
    config = {}

    mapping_is_set = False  # 判断是否已经设置了es的mapping

    def __init__(self, config):
        """
        es初始化
        配置参数：
        host: es连接字符串
        indexName: index的名字
        deleteIndex: 是否删除已经存在的index，默认为false，不删除
        settings: index的配置。具体的配置项，请看es的文档。
        settingsFile: index的配置，json文件。具体的配置项，请看es的文档。
        mappings: mappings的配置。具体的配置项，请看es的文档。
        mappingsFile: mappings的配置，json文件。具体的配置项，请看es的文档。
        idField: id字段。有些数据是包含id字段的

        说明：settings和settingsFile最多只能有一项
        mappings和mappingsFile最多也只能有一项
        """
        self.es = ElasticSearch(config['host'])

        if 'docType' not in config:
            config['docType'] = config['indexName']
        self.config = config

        if 'deleteIndex' in config and config['deleteIndex']:
            try:
                self.es.delete_index(config['indexName'])

                print('delete index ' + config['indexName'] + ' success!')
            except ElasticHttpNotFoundError:  # 如果本来不存在，则输出提示就好
                print('Index ' + config['indexName'] \
                                + ' not found, nothing to delete!')
            except:
                raise Exception('Index ' + config['indexName'] + ' delete error!')

        try:
            if 'settings' in config:
                self.es.create_index(config['indexName'],
                                     settings=config['settings'])
            elif 'settingsFile' in config:
                with open(config['settingsFile'], 'r') as f:
                    config['settings'] = json.loads(f.read())
                self.es.create_index(config['indexName'],
                                     settings=config['settings'])
            else:
                self.es.create_index(config['indexName'])

            print('create index ' + config['indexName'] + ' success!')
        except Exception:
            raise Exception("create index " + config['indexName'] + ' error!')

    def _putMapping(self, row):
        """
        设置es的mapping。
        可以根据row生成默认配置, 生成配置规则如下：
        """
        try:
            if 'mappingsFile' in self.config:
                with open(self.config['mappingsFile'], 'r') as f:
                    self.config['mappings'] = json.loads(f.read())

            if 'mappings' in self.config:
                self.es.put_mapping(self.config['indexName'],
                                    self.config['docType'],
                                    self.config['mappings'])
            print("put mapping " + self.config['indexName'] + ' success!')
        except Exception:
            raise Exception("put mapping " + self.config['indexName'] + ' error!')

    def read(self):
        pass

    def batchRead(self):
        pass

    def write(self, row):
        """
        写入单行记录
        """
        return self.batchWrite([row])

    def batchWrite(self, rows):
        """
        写入多行记录
        """
        if not self.mapping_is_set:   # 设置mapping
            self.mapping_is_set = True
            self._putMapping(rows[0])

        docs = ()
        if 'idField' in self.config:
            docs = (self.es.index_op(doc, id=doc.pop(self.config['idField'])) \
                    for doc in rows)
        else:
            docs = (self.es.index_op(doc) for doc in rows)

        self.es.bulk(docs,
                     index=self.config['indexName'],
                     doc_type=self.config['docType'])

        return True
