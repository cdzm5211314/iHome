# -*- coding:utf-8 -*-
# @Desc : 
# @Author : Administrator
# @Date : 2019-09-17 23:30

from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy
import redis  # 缓存 + session
from flask_session import Session  # 自定义session的存储位置,安装: pip install flask-session
from flask_wtf import CSRFProtect  # csrf防护机制


# 创建数据库SQLAlchemy工具对象
db = SQLAlchemy()

# 创建redis链接对象 - 缓存
redis_store = None


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


