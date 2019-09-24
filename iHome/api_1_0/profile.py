# -*- coding:utf-8 -*-
# @Desc : 
# @Author : Administrator
# @Date : 2019-09-23 19:47

from . import api
from flask import g, current_app, jsonify, request
from iHome.utils.commons import login_required
from iHome.utils.response_code import RET
from iHome.utils.image_storage import storage
from iHome.models import User
from iHome import db, constants


# POST http://127.0.0.1:5000/api/v1.0/users/avatar
@api.route("/users/avatar", methods=["POST"])
@login_required  # 设置用户图像的前提是用户必须是登录状态,所以加上登录验证装饰器
def set_user_avatar():
    """设置用户的头像
    参数: 图片(多媒体表单) 用户id(g对象,g.user_id)
    """
    # 获取参数
    user_id = g.user_id  # 登录验证装饰器代码中代码已经将user_id保存在g对象中,所以视图中可以直接读取
    image_file = request.files.get("avatar")

    # 验证参数
    # 验证图片是否上传
    if image_file is None:
        return jsonify(errno=RET.PARAMERR, errmsg="未上传图片")

    # 业务逻辑处理
    # 读取上传图片的数据
    image_data = image_file.read()
    # 调用七牛上传图片,若成功返回上传后的文件名字
    try:
        file_name = storage(image_data)
    except Exception as e:
        # 记录日志
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="上传图片失败")

    # 保存文件名到数据库中
    try:
        User.query.filter_by(id=user_id).update({"avatar_url": file_name})
        db.session.commit()
    except Exception as e:
        # 保存失败,事务回滚
        db.session.rollback()
        # 记录日志
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存图片信息失败")

    # 返回值
    avatar_url = constants.QINIU_URL_DOMAIN + file_name  # 拼接图片的路径
    return jsonify(errno=RET.OK, errmsg="保存成功", data={"avatar_url": avatar_url})
