# -*- coding:utf-8 -*-
# @Desc : flask配置文件
# @Author : Administrator
# @Date : 2019-09-17 23:10

import redis

class Config(object):
    '''配置参数信息 - 使用类的方式'''
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
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # redis的链接实例对象
    SESSION_USE_SIGNER = True  # 对cookie中的session_id进行隐藏加密处理
    PERMANENT_SESSION_LIFETIME = 86400  # session数据的有效期,单位秒



class DevelopmentConfig(Config):
    '''开发模式的配置信息'''
    DEBUG = True


class ProductConfig(Config):
    '''生产环境的配置信息'''
    pass

# 配置模式与类之间的映射关系
config_map = {
    'develop': DevelopmentConfig,
    'product': ProductConfig,
}