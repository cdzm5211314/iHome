# -*- coding:utf-8 -*-
# @Desc : 图片验证码与短信验证码
# @Author : Administrator
# @Date : 2019-09-20 20:05

from . import api
from iHome.utils.captcha.captcha import captcha
from iHome import redis_store, constants
from flask import current_app, jsonify, make_response
from iHome.utils.response_code import RET


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
        redis_store.setex("image_code_%s" %image_code_id, constants.IMAGE_CODE_REDIS_EXPIRE, text)
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


