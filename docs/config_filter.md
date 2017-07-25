#### 1.1 设置唯一约束 unique

```
transfrom:
  - type: filter
    name: unique
    field: fieldname
```

- `field`: 列名

#### 1.2 删除空行 empty
某字段为空字符串的话，则删除该行

```
transfrom:
  - type: filter
    name: empty
    field: fieldname
```

#### 1.3 字段值等于某值，则删除 eq

```
transfrom:
  - type: filter
    name: eq
    field: fieldname
    value: somevalue
```

#### 1.4 字段值在列表里，则删除 in

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
