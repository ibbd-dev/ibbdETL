# 数据输出目标配置：target
配置数据的输出部分，可以将数据输出到如下格式：

- [x] console: 控制台
- [x] csv: CSV格式
- [x] es: ElasticSearch
- [ ] mysql: Mysql数据库
- [ ] mongodb: MongoDB数据库
- [ ] json: 输出json的数据格式，需要先映射为宽表
- [ ] jsonAPI：向http的api接口输出数据，以json的格式。
- [ ]

### 2.1 通用参数说明

```
target:
  type: csv
  batch: false
  batchNum: 10
  params:
    filename: /var/log/test.csv
```

- `type`：定义输出类型，如csv等
- `batch`: [可选]取值为true or false，允许为空，默认为false。设置为true时，则启用批量写入功能。
- `batchNum`：[可选]每次批量输出的记录数量，必须和`batch`参数搭配使用。
- `params`：[可选]具体输出对象的配置，例如如果输出到csv文件中，则需要配置文件名等。

### 2.2 控制台输出：console
参数非常简单，只有一个分隔符可以定义，默认分隔符为Tab键。样例配置如下：

```
target:
  type: console
  params:
    delimiter: ','
```

注：delimiter是可选参数。

### 2.3 CSV文件输出：csv
输出csv文件：

```
target:
  type: csv
  params:
    filename: data/coord-output.csv
    delimiter: ','
```

1. `filename`: 定义输出的csv文件名
2. `delimiter`: 定义分隔符，允许为空，默认值为`,`

### 2.4 ElasticSearch输出：elasticsearch

```
target:
  type: elasticsearch
  batch: true
  batchNum: 1000
  params:
    host: 'http://localhost:9200/'
    indexName: test_jiangmen_coord
    deleteIndex: false
```

1. host: es服务器地址
2. indexName: 需要写入的index name
3. deleteIndex: 如果index name已经存在，是否删除旧的index
4. settings: index的配置。具体的配置项，请看es的文档。
5. settingsFile: index的配置，json文件。具体的配置项，请看es的文档。
6. mappings: mappings的配置。具体的配置项，请看es的文档。
7. mappingsFile: mappings的配置，json文件。具体的配置项，请看es的文档。
8. idField: id字段。有些数据是包含id字段的

说明：

- settings和settingsFile最多只能有一项
- mappings和mappingsFile最多也只能有一项

