# -*- coding: utf-8 -*-

# elasticsearch
# Author: Alex
# Created Time: 2017年05月22日 星期一 10时00分04秒
from pyelasticsearch import ElasticSearch
from pyelasticsearch import ElasticHttpNotFoundError


class IbbdElasticSearch:
    """
    es操作
    文档：http://pyelasticsearch.readthedocs.io/en/latest/
    """
    es = None
    config = {}

    def __init__(self, config):
        """
        es初始化
        配置参数：
        host: es连接字符串
        indexName: index的名字
        deleteIndex: 是否删除已经存在的index，默认为false，不删除
        settings: index的配置。具体的配置项，请看es的文档。
        idField: id字段。有些数据是包含id字段的
        """
        self.es = ElasticSearch(config['host'])

        if 'docType' not in config:
            config['docType'] = config['indexName']
        self.config = config

        if 'deleteIndex' in config and config['deleteIndex']:
            try:
                self.es.delete_index(config['indexName'])
            except ElasticHttpNotFoundError:
                raise Exception('Index ' + config['indexName'] \
                                + ' not found, nothing to delete')

            print('delete index ' + config['indexName'] + ' success!')

        try:
            if 'settings' in config:
                self.es.create_index(config['indexName'],
                                     settings=config['settings'])
            else:
                self.es.create_index(config['indexName'])
        except Exception:
            raise Exception("create index " + config['indexName'] + ' error!')

        print('create index ' + config['indexName'] + ' success!')

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
        docs = ()
        if 'idField' in self.config:
            docs = (self.es.index_op(doc, id=doc.pop(self.config['idField'])) \
                    for doc in rows)
        else:
            docs = (self.es.index_op(doc) for doc in rows)

        self.es.bulk(docs,
                     index_name=self.config['indexName'],
                     doc_type=self.config['docType'])

        return True
