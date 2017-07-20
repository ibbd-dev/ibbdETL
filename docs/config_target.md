# 数据输出目标配置：target
配置数据的输出部分，可以将数据输出到如下格式：

- [x] console: 控制台
- [x] csv: CSV格式
- [x] es: ElasticSearch
- [x] esMapping: 导出成es的mapping配置文件（json格式）
- [ ] mysql: Mysql数据库
- [ ] mongodb: MongoDB数据库
- [x] json: 输出json的数据格式，需要先映射为宽表
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
    indexName: merge_mp_20170524
    mappingsFile: conf/merge_mp.json
    deleteIndex: true
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

### 2.5 将数据格式化成es mapping的格式：esMapping
下面的配置是根据一个csv文件生成es mapping的json配置文件：

```
source:
  type: csv
  fieldNotMatch: keep
  params:
    filename: data/indexs_monitor_utf8.csv
    delimiter: ','

target:
  type: esMapping
  rowsLimit: 1
  params:
    filename: conf/indexs_monitor_es_mapping.json
```

注意：

- rowsLimit: 该参数表示只要第一行数据即可。
- 字符串字段默认不进行分词

前面只是根据第一行来推断字段的类型，但是这样可能会造成比较到的误差，例如当字段值为字符串的0时，这个时候可能是整型，也可能是浮点型，这种情况是经常存在的。根据多行来判断会靠谱一点，而且有些特殊的类型可以指定，如下：

```
source:
  type: csv
  fieldNotMatch: keep
  params:
    filename: data/indexs_monitor_utf8.csv
    delimiter: ','

target:
  type: esMapping
  rowsLimit: 1000
  params:
    filename: conf/indexs_monitor_es_mapping2.json
    fields:
    - name: 监测日期
      config:
        type: date
        format: "yyyy/MM/dd"
```

根据前1000来判断，并且指定了`监测日期`这个字段的配置。


### 2.6 将数据导出到MySQL：mysql

将数据写入 MySQL 数据库,需要预先创建表,字段应与输出的字段一致

```
target:
  type: mysql
  params:
    host: 127.0.0.1
    port: 3306
    user: root
    passwd: root
    db: test
    charset: utf8
    table: testmysql
    batch: true
    batchNum: 1000
```

- `host:` MySQL 主机地址
- `port:` MySQL 端口(可选参数,默认3306)
- `user:` 用户名
- `passwd:` 密码
- `db:` 数据库
- `table:` 表名
- `charset:` 字符集(可选参数,默认设置成UTF8)
- `batch`: 是否开启批量写入,默认 false
- `batchNum`: 一次写入 batchNum 条数据, batch 参数需要配置成 true 才可用

### 2.7 将数据导出到 json 文件：json
params 参数只需配置 filename 即可

```
target:
  type: json
  params:
    filename: jsonoutput.json
    encoding: utf8
```

- `filename:` json文件名
- `encoding`: 文件编码方式(可选参数，默认以 utf8 编码)


