# -*- coding:utf-8 -*-
# @Desc : 
# @Author : Administrator
# @Date : 2019-09-17 23:58

from . import api
from iHome import db


# 使用蓝图对象注册路由
@api.route('/index')
def index():
    return 'index page'


