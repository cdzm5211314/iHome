# -*- coding:utf-8 -*-
# @Desc : 
# @Author : Administrator
# @Date : 2019-09-19 20:35

from flask import Blueprint, current_app

# 创建提供静态文件的蓝图对象
html = Blueprint('web_html', __name__)


# http://127.0.0.1:5000/()
# http://127.0.0.1:5000/(index.html)
# http://127.0.0.1:5000/(register.html)
# http://127.0.0.1:5000/(favicon.ico)  # 浏览器认为的网站标识,浏览器会自己请求这个资源

# 3.直接在路由中使用自定义的万能正则转换器
@html.route('/<re(r".*"):html_file_name>')
def get_html(html_file_name):
    """提供html静态文件"""

    # 如果html_file_name参数值为空,表示访问的路径是/,请求的是主页
    if not html_file_name:
        html_file_name = 'index.html'

    # 注: send_static_file()方法默认是返回static目录下的文件,而我们这里是返回static/html目录下的文件,所以我们需要做拼接处理
    if html_file_name != 'favicon.ico':
        # 如果资源名不是favicon.ico,做拼接处理
        html_file_name = 'html/' + html_file_name

    # flask提供的专门用来返回静态文件的方法: send_static_file()
    return current_app.send_static_file(html_file_name)


