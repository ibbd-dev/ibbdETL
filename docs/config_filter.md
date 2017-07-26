# 行数据过滤
作用：行

对于满足某些条件的记录应该放弃掉，例如关键字段为空的时候，等等。实现condition如下：

- [x] `unique`: 为某字段设置唯一约束
- [x] `empty`: 某字段为空，则删除
- [x] `eq`: 等于某个值
- [x] `ne`: 不等于某个值
- [x] `gt`: 大于某个值
- [x] `gte`: 大于或者等于某个值
- [x] `lt`: 小于某个值
- [x] `lte`: 小于或者等于某个值
- [x] `in`: 在一个列表里
- [x] `nin`: 不在一个列表里
- [x] `match`: 满足或者不满足某正则表达式的，删除
- [] `example`:


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
- `len`: (可选参数)默认 false 数值比较; 若设置成 true ,则比较字段的长度


## 4 字段值不等于某值，则删除 ne

```
transfrom:
  - type: filter
    name: ne
    field: fieldname
    value: somevalue
    len: false
```
- `len`: (可选参数)默认 false 数值比较; 若设置成 true ,则比较字段的长度


## 5 某个字段的值大于某个值,则删除该行数据 gt

```
transfrom:
  - type: filter
    name: gt
    field: age
    value: 20
    len: false
```
- `len`: (可选参数)默认 false 数值比较; 若设置成 true ,则比较字段的长度


## 6 某个字段的值大于或等于某个值,则删除该行数据 gte

```
transfrom:
  - type: filter
    name: gte
    field: name
    value: 2
    len: true
```
- `len`: (可选参数)默认 false 数值比较; 若设置成 true ,则比较字段的长度


## 7 某个字段的值小于某个值,则删除该行数据 lt

```
transfrom:
  - type: filter
    name: lt
    field: age
    value: 10
    len: false
```
- `len`: (可选参数)默认 false 数值比较; 若设置成 true ,则比较字段的长度


## 8 某个字段的值小于或等于某个值,则删除该行数据 lte

```
transfrom:
  - type: filter
    name: lte
    field: age
    value: 20
    len: false
```
- `len`: (可选参数)默认 false 数值比较; 若设置成 true ,则比较字段的长度



## 9 字段值在列表里，则删除 in

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

## 10 字段值不在列表里，则删除 nin

```
transfrom:
  - type: filter
    name: nin
    field: fieldname
    values:
      - value: keepvalue
      - value: keepvalue2
      - value: keepvalue3
```


## 11 字段值满足某正则表达式的，删除或保留

```
transfrom:
  - type: filter
    name: match
    field: name
    pattern: ^[李]
    action: drop
```

某个字段的值满足某正则表达式的，则执行 action 操作,默认 drop 删除
- `field`: 字段名
- `action`: 可以设置成 keep 或 drop

- 设置成 keep 表示满足正则的都保留，不满足的都删除

- 设置成 drop 表示满足正则的都删除，不满足的都保留


