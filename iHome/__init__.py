# -*- coding:utf-8 -*-
# @Desc : 
# @Author : Administrator
# @Date : 2019-09-17 23:30

from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session  # 自定义session的存储位置,安装: pip install flask-session
from flask_wtf import CSRFProtect  # csrf防护机制
from logging.handlers import RotatingFileHandler

import redis  # 缓存 + session
import logging


# 创建数据库SQLAlchemy工具对象
db = SQLAlchemy()

# 创建redis链接对象 - 缓存
redis_store = None

# 配置日志信息
# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG)
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
# 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日记录器
logging.getLogger().addHandler(file_log_handler)


# 使用工厂模式,决定使用什么样配置参数信息创建app
def create_app(config_name):
    '''
    创建flask的应用对象
    :param config_name: str配置模式的名字 ('develop','product')
    :return:
    '''
    app = Flask(__name__)
    # 根据配置模式的名字获取配置参数的类
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)

    # 使用app初始化db
    db.init_app(app)

    # 初始化redis工具
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT)

    # 利用flask-session将session数据保存到redis中
    Session(app)

    # flask补充csrf防护
    CSRFProtect(app)

    # 注册蓝图
    from iHome import api_1_0  # 解决循环导入
    app.register_blueprint(api_1_0.api, url_prefix='/api/v1.0')

    return app


