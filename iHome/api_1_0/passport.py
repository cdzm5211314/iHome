# -*- coding:utf-8 -*-
# @Desc : 
# @Author : Administrator
# @Date : 2019-09-22 12:25

from . import api
from flask import request, jsonify, current_app, session
# from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from iHome.utils.response_code import RET
from iHome import redis_store, db,constants
from iHome.models import User

import re


# POST http://127.0.0.1:5000/api/v1.0/users/
@api.route('/users', methods=["POST"])
def register():
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
    print(mobile,sms_code,password,password2)
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
    # password_hash = generate_password_hash(password)  # 密码加密
    # user = User(name=mobile, password_hash=password_hash, mobile=mobile)
    user = User(name=mobile, password_hash=password, mobile=mobile)
    user.password = password  # 设置密码属性,即给密码进行加密
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


# POST http://127.0.0.1:5000/api/v1.0/sessions/
@api.route('/sessions', methods=["POST"])
def login():
    """用户登录
    请求参数: 手机号 密码
    参数格式: json
    """
    print "bbb"
    # 获取参数
    print request.get_json()
    req_dict = request.get_json()
    mobile = req_dict.get('mobile')
    password = req_dict.get('password')

    # 校验参数
    # 校验参数是否完整
    if not all([mobile, password]):
        # 参数信息不完整
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 校验手机号格式是否正确
    if not re.match(r'1[34578]\d{9}', mobile):
        # 手机格式不正确
        return jsonify(errno=RET.PARAMERR, errmsg="手机格式不正确")

    # 判断用户输入错误次数是否超过限制,如果超过限制,则不允许继续操作
    # redis记录: "access_nums_请求的IP":"次数"
    user_ip = request.remote_addr  # 用户请求的IP地址
    try:
        access_nums = redis_store.get("access_num_%s" % user_ip)
    except Exception as e:
        # 记录日志
        current_app.logger.error(e)
    else:
        if access_nums is not None and int(access_nums) >= constants.LOGIN_ERROR_MAX_TIMES:
            # redis中有记录并且错误次数大于5,阻止继续执行操作
            return jsonify(errno=RET.REQERR,errmsg="错误次数过多,请稍后重试")

    # 业务逻辑处理
    # 根据手机号从数据库查询用户的数据对象
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        # 记录日志
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取用户信息失败")

    # 用数据库中的密码与用户填写的密码进行对比验证是否一致
    if user is None or not user.check_password(password):
        # 如果登录验证失败,记录错误次数,返回信息
        try:
            redis_store.incr("access_num_%s" % user_ip)
            redis_store.expire("access_num_%s" % user_ip, constants.LOGIN_ERROR_FORBID_TIME)
        except Exception as e:
            # 记录日志
            current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="用户名或密码错误")

    # 如果登录验证相同,保存登录状态,在session中
    session["name"] = user.name
    session["mobile"] = user.mobile
    session["user_id"] = user.id

    # 返回值
    return jsonify(errno=RET.OK, errmsg="登录成功")


# GET http://127.0.0.1:5000/api/v1.0/session/
@api.route('/session', methods=["GET"])
def check_login():
    """检查登录状态"""
    # 尝试从session中获取用户的名字
    name = session.get("name")
    # 判断获取的name名字是否存在,存在说明已经登录,否则未登录
    if name is not None:
        return jsonify(errno=RET.OK, errmsg="true", data={"name":name})
    else:
        return jsonify(errno=RET.SESSIONERR, errmsg="false")


# DELETE http://127.0.0.1:5000/api/v1.0/session/
@api.route('/session', methods=["DELETE"])
def logout():
    """退出登录"""
    # 消除session数据
    session.clear()
    return jsonify(errno=RET.OK, errmsg="OK")


