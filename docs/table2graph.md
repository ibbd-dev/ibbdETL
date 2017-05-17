# 从宽表导入数据转化为图关系数据

## 图关系数据

原始数据：

name | age  | friend | other...
---- | ---- | ----   | ----
张三 | 20   | 李四   | 其他信息....

现在我们关注的字段是`name`, `age`和`friend`，梳理其关系如下：

- 有一个用户的name叫张三
- 张三的年龄是20
- 张三有一个叫李四的朋友

注意：在这里用户ID可以直接根据根据用户名hash而成

最终的图关系数据的格式是这样的，每一行的数据就是一组关系，格式如`{from实体}\t{关系}\t{to实体}\t.`

样例数据如下：

```
<u.11b6d3zr1j>	<name>	"张三"	.
<u.11b6d3zr1j>	<age>	"20"^^<xs:int>	.
<u.11b6dx6gcs>	<name>	"李四"	.
<u.11b6d3zr1j>	<friend>	<u.11b6dx6gcs>	.
```


如上图所示的三元组，说明：

- 关系：`name`, `age`, `friend`都是关系，使用`<>`前后标记
- 实体：`u.11b6dx6gcs`和`u.11b6d3zr1j`是用户ID，是实体，也使用`<>`前后标志。id类字段可以增加前缀
- 属性实体：如张三，李四和20（年龄），其实就是实体的属性
- 属性类型：如`^^<xs:int>`，表示该字段为整型。注：默认都是字符串

注：支持的属性类型见 https://docs.dgraph.io/v0.7.6/query-language/#rdf-types

## 转换的配置

转换的配置可以写成如下：

```
transform:
  - expand: graph
    relationships:
    - fromField: name
      toField: name
      isAttr: true
      relationship: name
    - fromField: name
      toField: age
      toType: int
      isAttr: true
      relationship: age
    - fromField: friend
      toField: friend
      isAttr: true
      relationship: name
    - fromField: name
      toField: friend
      relationship: friend
    - fromField: secondsupplier_hash
      toValue: bid
      isAttr: true
      relationship: company.type
    - fromField: secondsupplier_hash
      toField: thirdsupplier_hash
      relationship: compete
      isTwoWay: true
```

注：

- `Graph`: 关系转换名字。将宽表中的一行数据转换为多条图关系数据
- `relationshipMap`: 映射关系定义，定义为一个数组，每个元素定义一个关系，每个关系最终输出一行关系定义的字符串, 例如：`<u.11b6d3zr1j>	<name>	"张三"	.`, 使用`\t`进行分隔。
- `fromField`: from实体的字段名（对应宽表），如果字段名在宽表中不存在，则报错(下同)。toField设置类似
- `toValue`: to实体，将实体设置为指定的值，例如分类字段
- `toType`: 默认值为String，用来设置属性实体的值的类型
- `isAttr`: 定义是否为属性（to实体）
- `relationship`: 关系
- `isTwoWay`: 该关系是否为双向的（双向的关系有两条记录）

根据这样的配置就能将宽表数据转化为图关系数据。

注：字段需要做hash，增加前缀等，由外部完成

