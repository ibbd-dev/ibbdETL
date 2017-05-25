# -*- coding: utf-8 -*-

# ETL入口文件
# Author: Alex
# Created Time: 2017年05月16日 星期二 10时31分59秒

import click
import yaml

from src.source import Reader
from src.transform import Transform
from src.target import Target


__version__ = '0.5.2'


def main(config_file, console=False, debug=False):
    """
    数据清洗
    """
    with open(config_file) as f:
        config_data = yaml.load(f)
        reader = Reader(config_data['source'])

        target = None
        if not console:
            target = Target(config_data['target'])
        else:
            target = Target({'type': 'console'})

        transform = None
        if 'transform' in config_data:
            transform = Transform(config_data['transform'])

        for row in reader.next():
            if transform is not None:
                for row_new in transform.do(row):
                    target.write(row_new)
            else:
                target.write(row)


@click.command()
@click.option('--console', is_flag=True,
              help='指定输出到console，通常用在测试时')
@click.option('--debug/--no-debug', default=False,
              help='是否为测试状态，默认为否')
@click.argument('filename', type=click.Path(exists=True))
@click.version_option(version=__version__, help='版本信息')
def cli(filename, console, debug):
    """
    基于python3的数据清洗工具。

    \b
    基础使用方式:
        ibbdetl /path/to/config-file.yml
    直接将结果输出到控制台（通常测试时使用）:
        ibbdetl /path/to/config-file.yml --console
    """
    main(filename, console=console, debug=debug)


if __name__ == "__main__":
    cli()
