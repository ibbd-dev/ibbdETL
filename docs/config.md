# yml配置文件格式说明

目录：

1. source
2. target
3. transform

数据从source数据源读入，经过transform数据转换的各个组件进行处理，最后到达target进行输出。

## 1. source
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
- `fields`: 数据输入字段的规范化，例如数据类型转换等。该字段定义只需要定义有用的字段，其他的没有定义的字段将会被过滤掉。下层属性有：
  - `name`: 字段名称
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

## 2. target
配置数据的输出部分，可以将数据输出到如下格式：

- [x] console: 控制台
- [x] csv: CSV格式
- [ ] es: ElasticSearch
- [ ] mysql: Mysql数据库
- [ ] mongodb: MongoDB数据库
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

## 3. transform

### 3.1 数据过滤: filter
对于满足某些条件的记录应该放弃掉，例如关键字段为空的时候，等等。实现如下：

- [ ] `emptyDrop`: 某字段为空，则删除
- [ ] `compareDrop`: 某字段的值和某个值进行比较，若满足某条件则删除
- [ ] `lenDrop`: 字符串长度满足某条件的，删除
- [ ] `regularDrop`: 满足或者不满足某正则表达式的，删除
- [ ] `example`: 

### 3.2 字段修改：modifier
对字段的值进行修改。

- [x] `hash`: 对某字段做hash运算，通常用在实体标识字段或者数据脱敏上。
- [x] `addPrefix`: 给字段值增加前缀
- [x] `coordTransform`: 各种不同体系的经纬度坐标的转换
- [x] `type`: 数据类型转换，例如从整型转化为字符串等。
- [x] `template`: 按照模板生成新的字符串
- [x] `symbolic`: 符号计算，对字符串进行求值，可以结合`template`先处理成目标字符串，再求值。
- [ ] `example`: 

```
# python的模板字符串
a = {'name': 'world', 'message': 'hello world'}
print("hello {name} , your {name} message is {message} ".format(**a))
```

### 3.3 数据扩展：expand
对数据进行扩展，例如将本来一行的数据扩展成了2行甚至更多。

- [x] `graph`: 将宽表数据转化为图关系数据，见[文档](/docs/table2graph.md)
- [x] `split`: 将一个字段分拆成多行
- [ ] `example`: 


