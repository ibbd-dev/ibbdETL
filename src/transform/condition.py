# -*- coding: utf-8 -*-
# 条件
# Author: Alex
# Created Time: 2017年07月03日 星期二 10时44分37秒
import re


class Condition:
    """
    条件判断，配置格式如下:
    condition:
    - name: ge
      field: field
      not: false
      params:
        value: 10
    """
