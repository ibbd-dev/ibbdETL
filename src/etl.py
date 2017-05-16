# -*- coding: utf-8 -*-

# ETL入口文件
# Author: Alex
# Created Time: 2017年05月16日 星期二 10时31分59秒

import click
import yaml

from source import Reader
from transform import Transform
from target import Target


__version__ = '0.1.0'


@click.command()
@click.option('--config-file', required=True,
              help='配置文件')
@click.version_option(version=__version__, )
def cli(config_file):
    """
    数据清洗
    """
    with open(config_file) as f:
        config_data = yaml.load(f)
        reader = Reader(config_data['source'])
        transform = Transform(config_data['transform'])
        target = Target(config_data['target'])

        for row in reader.nextRow():
            for row_new in transform.do(row):
                target.write(row_new)


if __name__ == "__main__":
    cli()
