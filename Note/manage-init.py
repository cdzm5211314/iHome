# -*- coding:utf-8 -*-
# @Desc : 未拆分 - manage.py
# @Author : Administrator
# @Date : 2019-09-17 22:27

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session  # 自定义session的存储位置,安装: pip install flask-session
from flask_wtf import CSRFProtect  # csrf防护机制

import redis

app = Flask(__name__)

class Config(object):
    '''配置参数信息 - 使用类的方式'''
    DEBUG = True
    SECRET_KEY = 'a1s2d3f4g5h6j7k8l9'

    # 数据库
    # SQLAlchemy配置参数: 设置链接数据库的URL
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@127.0.0.1:3306/flaskdemo"
    # SQLAlchemy配置参数: 设置sqlalchemy自动更新跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLAlchemy配置参数: 数据库查询时显示原始SQL语句(程序调试的时候可以使用)
    SQLALCHEMY_ECHO = True

    # redis数据库信息 - 缓存
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # flask-session配置 - session
    SESSION_TYPE = 'redis'  # session的存储方式
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT,decode_responses=True)  # redis的链接实例对象
    SESSION_USE_SIGNER = True  # 对cookie中的session_id进行隐藏加密处理
    PERMANENT_SESSION_LIFETIME = 86400  # session数据的有效期,单位秒

app.config.from_object(Config)

# 创建数据库SQLAlchemy工具对象
db = SQLAlchemy(app)

# 创建redis链接对象 - 缓存
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

# 利用flask-session将session数据保存到redis中
Session(app)

# flask补充csrf防护
CSRFProtect(app)


@app.route('/index')
def index():

    return 'index page'


if __name__ == '__main__':
    app.run()


