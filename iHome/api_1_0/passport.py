# -*- coding:utf-8 -*-
# @Desc : 
# @Author : Administrator
# @Date : 2019-09-22 12:25

from . import api
from flask import request, jsonify, current_app, session
from iHome.utils.response_code import RET
from iHome import redis_store, db
from iHome.models import User
from sqlalchemy.exc import IntegrityError
import re


# GET http://127.0.0.1:5000/api/v1.0/users/
@api.route('/users')
def get_image_code():
    """"用户注册
    请求的参数: 手机号, 验证码, 密码, 确认密码
    参数格式: json
    """

    # 获取参数:
    # 获取请求的json数据,返回字典
    req_dict = request.get_json()
    mobile = req_dict.get('mobile')
    sms_code = req_dict.get('sms_code')
    password = req_dict.get('password')
    password2 = req_dict.get('password2')

    # 校验参数:
    # 校验参数是否完整
    if not all([mobile, sms_code, password, password2]):
        # 参数不完整
        return jsonify(errno=RET.PARAMERR, errmsg="参数信息不完整")

    # 校验手机格式是否正确
    if not re.match(r'1[34578]\d{9}', mobile):
        # 手机格式不正确
        return jsonify(errno=RET.PARAMERR, errmsg="手机格式不正确")

    # 校验两次密码是否一致
    if password != password2:
        # 两次密码不一致
        return jsonify(errno=RET.PARAMERR, errmsg="两次密码不一致")

    # 业务逻辑处理:
    # 从redis中取出短信验证码
    try:
        real_sms_code = redis_store.get("sms_code_%s" % mobile)
    except Exception as e:
        # 记录日志
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="读取真实短信验证码异常")

    # 判断从redis中取出的短信验证码是否过期
    if real_sms_code is None:
        return jsonify(errno=RET.NODATA, errmsg="短信验证码失效")

    # 删除redis中的短信验证码,防止重复使用校验
    try:
        redis_store.delete("sms_code_%s" % mobile)
    except Exception as e:
        # 记录日志
        current_app.logger.error(e)

    # 判断用户填写的短信验证码与从redis中取出的短信验证码是否一致
    if real_sms_code != sms_code:
        return jsonify(errno=RET.DATAERR, errmsg="短信验证码错误")

    # 判断用户手机号是否注册过
    # try:
    #     user = User.query.filter_by(mobile=mobile).first()
    # except Exception as e:
    #     # 记录日志
    #     current_app.logger.error(e)
    #     return jsonify(errno=RET.DBERR, errmsg="数据库异常")
    # else:
    #     if user is not None:
    #         # 表示手机号存在
    #         return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")

    # 保存用户注册信息到数据库
    user = User(name=mobile, password_hash=password, mobile=mobile)
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        # 数据库操作错误后的事务回滚
        db.session.rollback()
        # 记录日志, 表示手机号出现重复值,即手机号已被注册
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")
    except Exception as e:
        # 数据库操作错误后的事务回滚
        db.session.rollback()
        # 记录日志
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据库异常")

    # 保存登录状态到session中
    session['name'] = mobile
    session['mobile'] = mobile
    session['user_id'] = user.id

    # 返回值:
    return jsonify(errno=RET.OK, errmsg="注册成功")
