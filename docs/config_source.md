# 数据源配置：source

数据输入部分。数据源可以来自：

- [x] csv: CSV格式
- [ ] es: ElasticSearch
- [ ] mysql: Mysql数据库
- [ ] mongodb: MongoDB数据库
- [ ] 

### 1.1 通用参数说明
外层的参数有：

- `type`: 定义数据源的类型
- `params`: 定义数据源所需要的参数，例如csv的文件名等。不同的数据源只是该参数有所区别。
- `fieldNotMatch`: 字段在`fields`中如果没有被匹配，则执行什么操作，默认是`drop`（即丢弃），也可以修改为`keep`
- `fields`: 数据输入字段的规范化，例如数据类型转换等。该字段定义只需要定义有用的字段，其他的没有定义的字段将会被过滤掉。下层属性有：
  - [x] `name`: 字段名称
  - [x] `defaultValue`: 默认值（当字段值为空字符串时，允许指定默认值）
  - `type`: 字段的数据类型，允许为空，默认为`string`，支持如下格式：
    - [x] `string`: 默认
    - [x] `float`: 浮点数
    - [x] `int`: 整数
    - [ ] `date`: 日期格式，标准化为`2017-05-17`
    - [ ] `datetime`: 时间格式，标准化为`2017-05-17T20:33:20.000+08`

样例如下：

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



