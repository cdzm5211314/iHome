# -*- coding:utf-8 -*-
# @Desc : 
# @Author : Administrator
# @Date : 2019-09-28 21:00

from celery import Celery
from iHome.libs.yuntongxun.sms import CCP


# 发送短信验证码的celery任务

# 创建Celery对象
# 参数一: 随便定义一个能识别celery任务的名字
# 参数二: broker(中间人),存储celery任务 - 使用redis数据库
# Python2.7.15使用 celery + redis时注意版本号: 此处是 celery 3.1.25 redis 2.10.6
celery_app = Celery("iHome", broker="redis://127.0.0.1:6379/1")


@celery_app.task
def send_sms(to, datas, temp_id):
    """发送短信的异步任务"""
    ccp = CCP()
    ccp.send_Template_SMS(to, datas, temp_id)

# celery开启的命令
# celery -A iHome.tasks.task_sms worker -l info


