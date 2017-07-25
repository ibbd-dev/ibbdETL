# 字段数据修改 modifier
作用：字段

对字段的值进行修改。

- [x] `hash`: 对某字段做hash运算，通常用在实体标识字段或者数据脱敏上。
- [x] `addPrefix`: 给字段值增加前缀
- [x] `coordTransform`: 各种不同体系的经纬度坐标的转换
- [x] `type`: 数据类型转换，例如从整型转化为字符串等。
- [x] `template`: 按照模板生成新的字符串
- [x] `symbolic`: 符号计算，对字符串进行求值，可以结合`template`先处理成目标字符串，再求值。
- [x] `mapping`: 映射，将值映射为相应的值，特别适用于类别变量。
- [ ] `drop`: 删除某些字段
- [x] `replace`: 替换
- [ ] `if`: 可以对字段做if-else分支运算
- [ ] `example`:

## 2.1 hash

```
  - type: modifier
    name: hash
    field: name
    newField: name_hash
    len: 10
```

解读：对name字段做hash运算，取前10个字符，并将结果保存到name_hash字段。

## 2.2 addPrefix

```
  - type: modifier
    name: addPrefix
    field: name
    newField: name_id
    prefix: 'u.'
```

给name字段的值加上前缀`u.`，并将结果保存到新字段name_id中（新字段名如果不定义，则覆盖原来的值）

## 2.3 coordTransform

```
  - type: modifier
    name: coordTransform
    from:
      type: wgs84
      latField: lat
      lngField: lng
    to:
      type: bd09
      latField: lat
      lngField: lng
```

将wgs84的地理坐标系转化为bd09坐标系，处理前的坐标系字段为lng,lat，处理后的字段也为lng,lat

## 2.4 type
## 2.5 template

```
  - type: modifier
    name: template
    field: ID
    template: "{加密号码}_{ID}"
```

将`加密号码`和`ID`这两个字段的值按`template`定义的格式连接成新的字符串，保存到`ID`字段中。

## 2.6 symbolic
## 2.7 mapping

```
  - type: modifier
    name: mapping
    from: 期次
    to: ID
    default: 0
    mappings:
    - from: '第一期'
      to: 1
    - from: '第二期'
      to: 2
    - from: '第三期'
      to: 3
```

将字段`期次`的值按照`mappings`的定义映射到新字段`ID`，如果原字段的值不满足映射规则，则新值默认为0.

## 2.8 drop

## 2.9 replace

```
  - type: modifier
    name: replace
    field: 监测日期
    newField: new_fieldname
    useRe: true
    old: "(\\d+)月(\\d+)日"
    new: "2017-\\1-\\2"
```

注：

- useRe: 是否使用正则表达式，默认为false
- old和new可以支持正则匹配，具体有参数useRe决定（默认不使用正则）
- newField: 该参数可选，默认与field参数一致




