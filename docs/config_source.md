# 数据源配置：source

数据输入部分。数据源可以来自：

- [x] csv: CSV格式
- [ ] es: ElasticSearch
- [x] mysql: Mysql数据库
- [ ] mongodb: MongoDB数据库
- [x] json: 输入json的数据格式，需要先映射为宽表
- [x] jsonAPI：从http的api接口读取数据，以json的格式。
- [ ]

### 1.1 通用参数说明
外层的参数有：

- `type`: 定义数据源的类型
- `params`: 定义数据源所需要的参数，例如csv的文件名等。不同的数据源只是该参数有所区别。
- `fieldsNameMap`: 字段名格式化，例如字段名包含了特殊字符，但是在某些数据库中字段名却可能不能包含某些特殊字符
  -  [x] `replace`: 字符串替换
- `fieldNotMatch`: 字段在`fields`中如果没有被匹配，则执行什么操作，默认是`drop`（即丢弃），也可以修改为`keep`
- `fields`: 数据输入字段的规范化，例如数据类型转换等。该字段定义只需要定义有用的字段，其他的没有定义的字段将会被过滤掉。下层属性有：
  - [x] `name`: 字段名称
  - [x] `fieldMatch`: 使用正则来匹配字段。这样就可以批量处理字段。
  - [x] `defaultValue`: 默认值（当字段值为空字符串时，允许指定默认值）
  - [x] `trim`: 是否去掉字符串前后的空格（默认值false不做处理），取值true or false
  - `type`: 字段的数据类型，允许为空，默认为`string`，支持如下格式：
    - [x] `string`: 默认
    - [x] `float`: 浮点数
    - [x] `int`: 整数
    - [x] `date`: 日期格式，标准化为`2017-05-17`
    - [ ] `datetime`: 时间格式，标准化为`2017-05-17T20:33:20.000+08`

#### 样例如下：

```
source:
  type: csv
  params:
    filename: data/coord.csv
  fieldNotMatch: drop
  fields:
  - name: lng
    type: float
  - name: lat
    type: float
```

#### 批量修改字段：（使用正则表达式）

```
  fields:
  - fieldMatch: '^av_.*'
    type: float
    trim: true
    defaultValue: 0
```


#### 从两个数据源通过关联读取数据

```
source:
  type: csv
  params:
    filename: input.csv
    encoding: gbk
  fields:
  - name: id
  - name: name

joinSource:
  type: csv
  params:
    filename: joinSource.csv
    encoding: gbk
  fields:
  - name: user_id
  - name: email

  leftField: id
  rightField: user_id

target:
  type: csv
  params:
    filename: output.csv
```

- `joinSource`: 继承 source 所有特性
- `leftField`: source 的一个 Field, 与 `rightField` 进行关联
- `rightField`: joinSource 的一个 Field 与 `leftField` 进行关联


### 1.2 CSV文件格式: csv
参数只说明`params`部分，如：

```
  params:
    filename: data/coord.csv
    delimiter: ','
```

- `filename`: 定义csv文件的路径
- `delimiter`: 定义csv文件中的字段分隔符

注：现在csv数据源尚未支持定义表头。
注：从csv读出来的数据都是字符串，通常应该用trim去掉前后的空格，再设置一个默认值

### 1.3 MySQL数据库配置: mysql
从 MySQL 数据库读取数据: 参数只说明`params`部分，如：

```
source:
  type: mysql
  params:
    host: 127.0.0.1
    port: 3306
    user: root
    passwd: root
    db: test
    charset: utf8
    table: testmysql
    batchNum: 1000
    fields:
      - id
      - name
      - email
      - age
```

- `host`: MySQL 主机地址
- `port`: MySQL 端口(可选参数,默认3306)
- `user`: 用户名
- `passwd`: 密码
- `db`: 数据库
- `table`: 表名
- `charset`: 字符集(可选参数,默认设置成UTF8)
- `batchNum`: 批量从数据库读取数据,默认每1000条来读取
- `fields`: 需要读取的列名,默认SELECT * FROM table


### 1.4 json 配置: json
从 json 读取数据,如:

```
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
```

- `filename`: 若从文件中读取 json 数据,则配置成 json 文件路径
- `url`: 若从 URL 获取 json 数据,则配置成如 http://www.xxx.com/api

- 注意: filename 和 url 参数只能选取其中一个进行配置

- `encoding`: 文件/网页的编码方式,如 utf8 gbk 等
- `root`: 目标数据支持迭代的 json 根节点,假若目标数据在 json 的一个列表里,如json['weatherinfo']['recent'],此时应设置成 weatherinfo.recent
- `fields`: 目标字段
- `- name`: 字段名
- `  path`: 该字段的路径
