# -*- coding:utf-8 -*-
# @Desc : main.py作为celery启动模块
# @Author : Administrator
# @Date : 2019-09-28 21:28

from celery import Celery
from iHome.tasks import config

# 创建Celery对象
# 参数一: 随便定义一个能识别celery任务的名字
# 参数二: broker(中间人),存储celery任务 - 使用redis数据库

# Python2.7.15使用 celery + redis时注意版本号: 此处是 celery 3.1.25 redis 2.10.6
# celery_app = Celery("iHome", broker="redis://127.0.0.1:6379/1")
celery_app = Celery("iHome")

# 引入配置信息
# celery_app.config_from_object(config)
# celery目录结构方式时,windows系统适用字符串这种方式
celery_app.config_from_object("iHome.tasks.config")

# 自动搜寻异步任务
celery_app.autodiscover_tasks(["iHome.tasks.sms"])


# celery开启命令
# celery -A iHome.tasks.main worker -l info

