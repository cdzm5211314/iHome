# -*- coding:utf-8 -*-
# @Desc : 图片验证码与短信验证码
# @Author : Administrator
# @Date : 2019-09-20 20:05

from . import api
from iHome.utils.captcha.captcha import captcha
from iHome import redis_store, constants, db
from flask import current_app, jsonify, make_response, request
from iHome.utils.response_code import RET
from iHome.models import User
from iHome.libs.yuntongxun.sms import CCP
import random


# GET http://127.0.0.1:5000/api/v1.0/image_codes/<image_code_id>
@api.route('/image_codes/<image_code_id>')
def get_image_code(image_code_id):
    """
    获取图片验证码
    :param image_code_id: 图片验证码编号
    :return: 正常:返回验证码图片 异常:返回Json数据
    """
    # 1.获取参数
    # 2.校验参数
    # 3.业务逻辑处理
    # 生成验证码图片
    # 名字 真实文本 图片数据
    name, text, image_data = captcha.generate_captcha()
    # 将验证码真实值与编号保存到redis中,设置有效期
    # redis中的数据类型: 字符串(string) 列表(list) 哈希(hash) 集合(set) 有序集合(zset)
    # 如: key-value(字符串), key-value(列表), key-value(哈希), key-value(集合), key-value(有序集合)
    # 使用哈希维护有效期的时候只能整体设置
    # redis保存数据类型key-value(哈希),"image_code":{"id1":"vaule1","id2":"vaule2"} ---> 添加数据: hset("image_code", name, text)

    # 单条维护记录,使用字符串类型,如 "image_code_编号":"真实文本值"
    # redis_store.set("image_code_%s" %image_code_id, text)  # 保存验证码数据到redis中
    # redis_store.expire("image_code_%s" %image_code_id, constants.IMAGE_CODE_REDIS_EXPIRE) # 设置保存的验证码数据的有效期
    try:
        redis_store.setex("image_code_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRE, text)
    except Exception as e:
        # 把捕获的异常信息写入到日志文件中
        current_app.logger.error(e)
        # return jsonify(errno=RET.DATAERR, errmsg="save image code id failed")
        return jsonify(erron=RET.DATAERR, errmsg="图片验证码保存失败")

    # 4.返回值
    # 返回图片
    resp = make_response(image_data)
    resp.headers['Content-Type'] = "image/jpg"
    return resp


# GET http://127.0.0.1:5000/api/v1.0/sms_codes/<mobile>?image_code=xxx&image_code_id=yyy
@api.route('/sms_codes/<re(r"1[34578]\d{9}"):mobile>')
def get_sms_code(mobile):
    """获取短信验证码"""

    # 1.获取参数
    image_code = request.args.get("image_code")
    image_code_id = request.args.get("image_code_id")

    # 2.校验参数
    # 参数是否完整
    if not all([image_code, image_code_id]):
        # 表示参数不完整
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    # 3.业务逻辑处理
    # 从redis中获取真实的图片验证码值
    try:
        real_image_code = redis_store.get("image_code_%s" % image_code_id)
    except Exception as e:
        # 记录日志
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="redis数据库异常")

    # 判断获取的真实图片验证码是否过期
    if real_image_code is None:
        # 表示图片验证码没有或过期
        return jsonify(errno=RET.NODATA, errmsg="图片验证码失效")

    # 删除redis中的图片验证码: 防止用户使用同一个图片验证码验证多次(使用多次)
    try:
        redis_store.delete("image_code_%s" % image_code_id)
    except Exception as e:
        # 记录日志
        current_app.logger.error(e)

    # 与用户填写的验证码进行对比
    if real_image_code.lower() != image_code.lower():
        # 表示用户填写错误
        return jsonify(errno=RET.DATAERR, errmsg="图片验证码错误")

    # 判断注册的手机号是否存在
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        # 记录日志
        current_app.logger.error(e)
    else:
        if user is not None:
            # 表示手机号存在
            return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")

    # 如果手机号不存在,则生成短信验证码
    sms_code = "%06d" % random.randint(0, 999999)

    # 保存真实的短信验证码到redis中
    try:
        redis_store.setex("sms_code_%s" %mobile, constants.SMS_CODE_REDIS_EXPIRE, sms_code)
    except Exception as e:
        # 记录日志
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="保存短信验证码异常")

    # 发送短信
    try:
        cpp = CCP()
        result = cpp.send_Template_SMS(mobile, [sms_code, int(constants.SMS_CODE_REDIS_EXPIRE/60)], 1)
    except Exception as e:
        # 记录日志
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="发送异常")

    # 4.返回值
    if result == 0:
        # 表示短信发送成功
        return jsonify(errno=RET.OK, errmsg="发送成功")
    else:
        # 表示短信发送失败
        return jsonify(errno=RET.THIRDERR, errmsg="发送失败")


