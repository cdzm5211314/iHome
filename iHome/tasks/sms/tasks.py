# -*- coding:utf-8 -*-
# @Desc : 
# @Author : Administrator
# @Date : 2019-09-28 21:32


from iHome.libs.yuntongxun.sms import CCP
from iHome.tasks.main import celery_app

# 发送短信验证码的celery任务
@celery_app.task
def send_sms(to, datas, temp_id):
    """发送短信的异步任务"""
    ccp = CCP()
    ccp.send_Template_SMS(to, datas, temp_id)
