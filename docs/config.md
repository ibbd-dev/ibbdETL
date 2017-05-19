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
对于满足某些条件的记录应该放弃掉，例如关键字段为空的时候，等等。实现如下：

- [ ] `emptyDrop`: 某字段为空，则删除
- [ ] `compareDrop`: 某字段的值和某个值进行比较，若满足某条件则删除
- [ ] `lenDrop`: 字符串长度满足某条件的，删除
- [ ] `regularDrop`: 满足或者不满足某正则表达式的，删除
- [ ] `example`: 

### 2. 字段修改：modifier
对字段的值进行修改。

- [x] `hash`: 对某字段做hash运算，通常用在实体标识字段或者数据脱敏上。
- [x] `addPrefix`: 给字段值增加前缀
- [x] `coordTransform`: 各种不同体系的经纬度坐标的转换
- [x] `type`: 数据类型转换，例如从整型转化为字符串等。
- [x] `template`: 按照模板生成新的字符串
- [x] `symbolic`: 符号计算，对字符串进行求值，可以结合`template`先处理成目标字符串，再求值。
- [x] `mapping`: 映射，将值映射为相应的值，特别适用于类别变量。
- [ ] `example`: 


### 3. 数据扩展：expand
对数据进行扩展，例如将本来一行的数据扩展成了2行甚至更多。

- [x] `graph`: 将宽表数据转化为图关系数据，见[文档](/docs/table2graph.md)
- [x] `split`: 将一个字段分拆成多行
- [ ] `example`: 

### 4. 自定义处理：user
有些数据处理过程没有涵盖在标准化的过程里，需要用程序进行处理




