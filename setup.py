# -*- coding: utf-8 -*-

#
# Author: Alex
# Created Time: 2017年05月23日 星期二 10时17分06秒


from setuptools import setup, find_packages

version = '0.6.1'

setup(
    name='ibbdETL',
    version=version,
    description="ibbd ETL 数据清洗工具",
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'ibbdetl = src.etl:cli',
        ],
    },
    author='Alex Cai',
    author_email='cyy0523xc@gmail.com',
    license='GPL',
    install_requires=[
        'click',
        'pyyaml',
        'pyelasticsearch',
        'requests',
        'pymysql'
    ],
    test_suite="tests"
)
