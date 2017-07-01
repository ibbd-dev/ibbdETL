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
        lang: short_name
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
        facets:
        - name: start_year
          field: start_year
        - name: last_date
          field: last_date
    """
    config = {}

    # 属性允许的数据类型
    toTypes = ['string', 'int', 'float', 'double', 'boolean', 'date', 'dateTime', 'geojson']

    def __init__(self, config):
        for r in config['relationships']:
            if not('toField' in r or 'toValue' in r):
                raise Exception("to value not exist!")
            if not('relationship' in r or 'relationshipField' in r):
                raise Exception("relationship not exist!")
            if 'isAttr' not in r:
                r['isAttr'] = False

            if 'isTwoWay' not in r:
                r['isTwoWay'] = False

        self.config = config

    def do(self, rows):
        config = self.config
        data = []
        for row in rows:
            for relation in config['relationships']:
                res = {
                    'from': row[relation['fromField']].strip(),
                }

                # to的值允许直接指定，例如类型
                if 'toField' in relation:
                    res['to'] = row[relation['toField']]
                else:
                    res['to'] = relation['toValue']

                if len(res['from']) == 0 or len(res['to']) == 0:
                    # 过滤掉空的数据
                    continue

                res['from'] = u"<%s>" % res['from']
                res['to'] = self._parseToNode(res['to'], relation)

                # 定义关系
                if 'relationship' in relation:
                    res['relationship'] = u"<%s>" % relation['relationship']
                else:
                    res['relationship'] = u"<%s>" % row[relation['relationshipField']]

                # 定义边的属性，格式如：<alice> <car> "MA0123" (since=2006-02-02T13:01:09, first=true) .
                res['facets'] = ''
                if 'facets' in relation:
                    res['facets'] = self._parseFacets(row, relation['facets'])

                for i in self._output(res, relation):
                    data.append([i])

        return data

    def _output(self, res, relation):
        """格式化输出：<alice> <car> "MA0123" (since=2006-02-02T13:01:09, first=true) ."""
        if res['facets']:   # 有属性时的输出
            yield "%s\t%s\t%s\t%s\t." % \
                (res['from'], res['relationship'], res['to'], res['facets'])
            if relation['isTwoWay']:
                # 是否为双向关系
                yield "%s\t%s\t%s\t%s\t." % \
                    (res['to'], res['relationship'], res['from'], res['facets'])

        else:  # 没有属性时的输出
            yield "%s\t%s\t%s\t." % \
                (res['from'], res['relationship'], res['to'])
            if 'isTwoWay' in relation and relation['isTwoWay']:
                # 是否为双向关系
                yield "%s\t%s\t%s\t." % \
                    (res['to'], res['relationship'], res['from'])

    def _parseToNodeVal(self, to_val, to_type):
        """
        TODO: to_type: to字段的类型，支持如下值:
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
            return '"%s"^^<geo:geojson>' % to_val
        elif to_type == 'int':
            to_val = str(int(to_val))
        elif to_type == 'float' or to_type == 'double':
            to_val = str(float(to_val))

        return '"%s"^^<xs:%s>' % (to_val, to_type)

    def _parseToNode(self, to_val, relation):
        """解释to node"""
        to_str = ""
        if relation['isAttr']:
            if 'toType' in relation and relation['toType'] != 'string':
                # 定义类型
                to_str = self._parseToNodeVal(to_val, relation['toType'])
            elif 'lang' in relation:   # string类型可以定义语言
                to_str = '"%s"@%s' % (to_val, relation['lang'])
            else:
                to_str = '"%s"' % to_val

        else:
            to_str = '<%s>' % to_val

        return to_str

    def _parseFacets(self, row, facets):
        """解释边的属性: (since=2006-02-02T13:01:09, first=true) 
        注：相应的字段有值时，才会有相应的权重
        """
        facets_str = ['%s="%s"' % (f['name'], str(row[f['field']]))
                      for f in facets if row[f['field']]]
        if len(facets_str) > 0:
            return "(%s)" % ', '.join(facets_str)

        return ""
