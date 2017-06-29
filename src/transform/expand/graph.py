# -*- coding: utf-8 -*-

# 将宽表转化为图关系数据
# Author: Alex
# Created Time: 2017年05月16日 星期二 14时14分06秒


class Transform:
    """
    配置样例：
    - expand: graph
      relationships:
      - fromField: name
        toField: name
        isAttr: true
        relationship: name
      - fromField: name
        toField: age
        toType: Int
        isAttr: true
        relationship: age
      - fromField: friend
        toField: friend
        isAttr: true
        relationship: name
      - fromField: name
        toField: friend
        relationship: friend
        isTwoWay: true
        weights:
        - name: start_year
          field: start_year
        - name: last_date
          field: last_date
    """
    config = {}

    # 属性允许的数据类型
    toTypes = ['string', 'int', 'float', 'double', 'boolean', 'date', 'dateTime', 'geojson']

    def __init__(self, config):
        self.config = config

    def do(self, rows):
        config = self.config
        data = []
        for row in rows:
            for relation in config['relationships']:
                res = {
                    'from': row[relation['fromField']].strip(),
                    'relationship': relation['relationship'],
                }

                # to的值允许直接指定，例如类型
                if 'toField' in relation:
                    res['to'] = row[relation['toField']]
                elif 'toValue' in relation:
                    res['to'] = relation['toValue']
                else:
                    raise Exception("to value not exist!")

                if len(res['from']) == 0 or len(res['to']) == 0:
                    # 过滤掉空的数据
                    continue

                res['from'] = u"<%s>" % res['from']
                res['relationship'] = u"<%s>" % res['relationship']
                if 'isAttr' in relation and relation['isAttr']:
                    if 'toType' in relation:
                        res['to'] = u"\"%s\"%s" % (res['to'], self._parseType(relation['toType']))
                    else:
                        res['to'] = u"\"%s\"" % res['to']

                else:
                    res['to'] = u"<%s>" % res['to']

                # 定义边的权重，格式如：<alice> <car> "MA0123" (since=2006-02-02T13:01:09, first=true) .
                res['weights'] = ''
                if 'weights' in relation:
                    res['weights'] = self._parseWeights(row, relation['weights'])

                for i in self._output(res, relation):
                    data.append([i])

        return data

    def _output(self, res, relation):
        """格式化输出：<alice> <car> "MA0123" (since=2006-02-02T13:01:09, first=true) ."""
        if res['weights']:   # 有权重时的输出
            yield "%s\t%s\t%s\t%s\t." % \
                        (res['from'], res['relationship'], res['to'], res['weights'])
            if 'isTwoWay' in relation and relation['isTwoWay']:
                # 是否为双向关系
                yield "%s\t%s\t%s\t%s\t." % \
                            (res['to'], res['relationship'], res['from'], res['weights'])

        else:  # 没有权重时的输出
            yield "%s\t%s\t%s\t." % \
                        (res['from'], res['relationship'], res['to'])
            if 'isTwoWay' in relation and relation['isTwoWay']:
                # 是否为双向关系
                yield "%s\t%s\t%s\t." % \
                            (res['to'], res['relationship'], res['from'])

    def _parseType(self, to_type):
        """
        to_type: to字段的类型，支持如下值:
            string
            int
            float
            double
            boolean
            date
            dateTime
            geojson
        """
        if to_type == 'geojson':
            return '^^<geo:geojson>'
        return '^^<xs:%s>' % to_type

    def _parseWeights(self, row, weights):
        """解释边的权重: (since=2006-02-02T13:01:09, first=true) 
        注：相应的字段有值时，才会有相应的权重
        """
        weights_str = ["%s=%s" % (w['name'], str(row[w['field']]))
                       for w in weights if row[w['field']]]
        if len(weights_str) > 0:
            return "(%s)" % ', '.join(weights_str)
        return ""
