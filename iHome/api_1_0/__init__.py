# -*- coding:utf-8 -*-
# @Desc : 按照版本号的形式进行蓝图拆分
# @Author : Administrator
# @Date : 2019-09-17 23:57

from flask import Blueprint

# 创建蓝图对象
api = Blueprint('api_1_0',__name__)

# 导入蓝图的视图
from . import demo, verify_code, passport


