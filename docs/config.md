# yml配置文件格式说明
数据从source数据源读入，经过transform数据转换的各个组件进行处理，最后到达target进行输出。

数据输入输出相关的配置见文档：

1. [数据源配置](/docs/config_source.md)
2. [数据输出目标配置](/docs/config_target.md)

这里主要讲数据处理部分：transform


## transform
目录：

1. 数据过滤: filter：根据条件判断某行数据是否应该保留
2. 字段修改：modifier：针对某个字段的修改行为
3. 数据扩展：expand：将一行数据扩展为多行数据
4. 自定义处理：user: 自定义处理函数

### 1. 数据过滤: filter
作用：行

[数据过滤配置](/docs/config_filter.md)


### 2. 字段修改：modifier

[见文档](/docs/config_modifier.md)

### 3. 数据扩展：expand
作用：行

对数据进行扩展，例如将本来一行的数据扩展成了2行甚至更多。

- [x] `graph`: 将宽表数据转化为图关系数据，见[文档](/docs/table2graph.md)
- [x] `split`: 将一个字段分拆成多行
- [ ] `example`:

#### 3.1 graph
[见文档](/docs/table2graph.md)

### 4. 自定义处理：user
有些数据处理过程没有涵盖在标准化的过程里，需要用程序进行处理

```
transfrom:
  - type: user
    path: ./example.py
    func: change_time
```
- `path`: python文件路径
- `func`: 函数名

函数 `func` 接收一个由 collections.OrderedDict 组成的列表,每一个元素包含一行记录

返回一个处理后的由 collections.OrderedDict 组成的列表

### 5. 条件：condition


