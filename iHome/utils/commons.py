# -*- coding:utf-8 -*-
# @Desc : 
# @Author : Administrator
# @Date : 2019-09-19 21:31

from werkzeug.routing import BaseConverter
from flask import session, jsonify, g
from iHome.utils.response_code import RET
import functools

# 自定义万能正则转换器
# 1.自定义万能正则转换器类,需要继承 from werkzeug.routing import BaseConverter
class RegexConverter(BaseConverter):
    '''万能正则转换器'''

    def __init__(self, url_map, regex):  # url_map是固定参数,表示全局app对像的路由映射列表
        super(RegexConverter, self).__init__(url_map)  # 调用父类的初始化方法
        # 将正则表达式的参数保存到对象的属性中,Flask会使用这个属性来进行正则匹配
        self.regex = regex  # regex为url路由传递过来的正则表达式参数


# 登录验证装饰器
def login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        # 判断用户的登录状态
        user_id = session.get("user_id")
        if user_id is not None:
            # 如果用户已经登录,放行-执行视图函数
            g.user_id = user_id  # 将user_id保存到g对象当中,在视图函数中可以通过g对象获取保存的数据
            return view_func(*args, **kwargs)
        else:
            # 如果用户未登录,返回未登录的信息
            return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")
    return wrapper

