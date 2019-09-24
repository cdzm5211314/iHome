# -*- coding:utf-8 -*-
# @Desc : 项目工程中约定好常量值
# @Author : Administrator
# @Date : 2019-09-20 21:58


# 图片验证码的redis有效期,秒
IMAGE_CODE_REDIS_EXPIRE = 180

# 短信验证码的redis有效期,秒
SMS_CODE_REDIS_EXPIRE = 300

# 发送短信验证码的间隔时间,秒
SEND_SMS_CODE_INTERVAL = 60

# 登录错误尝试次数
LOGIN_ERROR_MAX_TIMES = 5

# 登录错误的限制时间,秒
LOGIN_ERROR_FORBID_TIME = 600

# 七牛的域名
QINIU_URL_DOMAIN = "http://pybuvc2az.bkt.clouddn.com/"


