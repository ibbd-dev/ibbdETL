# IbbdETL
通用的etl工具：通过写配置文件，实现数据的ETL。

## 安装及使用

```sh
# install
python3 setup.py install

# 帮助
ibbdetl --help

# 下面是两种使用方式
ibbdetl -c /path/to/config_file.yml
ibbdetl --config-file=/path/to/config_file.yml
```

## demo
见项目：https://github.com/ibbd-dev/ibbdETL-demos

## 开发过程使用

```sh
python3 src/etl.py --config-file=conf/hello.yml
```

## 文档

- 目录：`./docs/`
- 配置文件格式说明文档：`./docs/config.md`
- 模块开发说明文档：`./docs/dev.md`

