# -*- coding:utf-8 -*-
# @Desc : 
# @Author : Administrator
# @Date : 2019-09-19 21:31

from werkzeug.routing import BaseConverter


# 自定义万能正则转换器
# 1.自定义万能正则转换器类,需要继承 from werkzeug.routing import BaseConverter
class RegexConverter(BaseConverter):
    '''万能正则转换器'''

    def __init__(self, url_map, regex):  # url_map是固定参数,表示全局app对像的路由映射列表
        super(RegexConverter, self).__init__(url_map)  # 调用父类的初始化方法
        # 将正则表达式的参数保存到对象的属性中,Flask会使用这个属性来进行正则匹配
        self.regex = regex  # regex为url路由传递过来的正则表达式参数


