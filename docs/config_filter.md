# 行数据过滤
作用：行

对于满足某些条件的记录应该放弃掉，例如关键字段为空的时候，等等。实现condition如下：

- [x] `unique`: 为某字段设置唯一约束
- [x] `empty`: 某字段为空，则删除
- [ ] `match`: 满足或者不满足某正则表达式的，删除
- [x] `eq`: 等于某个值
- [ ] `ne`: 不等于某个值
- [ ] `gt`: 大于某个值
- [ ] `gte`: 大于或者等于某个值
- [ ] `lt`: 小于某个值
- [ ] `lte`: 小于或者等于某个值
- [x] `in`: 在一个列表里
- [ ] `nin`: 不在一个列表里
- [ ] `example`:


数据过滤相关的配置见文档：

## 1 设置唯一约束 unique

```
transfrom:
  - type: filter
    name: unique
    field: fieldname
```

- `field`: 列名

## 2 删除空行 empty
某字段为空字符串的话，则删除该行

```
transfrom:
  - type: filter
    name: empty
    field: fieldname
```

## 3 字段值等于某值，则删除 eq

```
transfrom:
  - type: filter
    name: eq
    field: fieldname
    value: somevalue
    len: true
```

- len: 默认false，如果为true的话，则先对字段值计算长度

## 4 字段值在列表里，则删除 in

```
transfrom:
  - type: filter
    name: in
    field: fieldname
    values:
    - value: dropvalue
    - value: dropvalue2
    - value: dorpvalue3
```
