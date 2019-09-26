# -*- coding:utf-8 -*-
# @Desc : 
# @Author : Administrator
# @Date : 2019-09-26 18:48

import json

from . import api
from flask import current_app, jsonify
from iHome.utils.response_code import RET
from iHome.models import Area
from iHome import constants, redis_store


# GET http://127.0.0.1:5000/api/v1.0/areas
@api.route("/areas")
def get_area_info():
    """获取城区信息"""

    # 先从redis缓存中获取城区信息
    try:
        resp_json = redis_store.get("area_info")
    except Exception as e:
        current_app.logger.error(e)
    else:
        if resp_json is not None:
            # redis中有缓存数据
            current_app.logger.info("hit redis area_info")
            return resp_json, 200, {"Content-Type": "application/json"}

    # 查询数据库,读取城区信息
    try:
        area_li = Area.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库异常")

    # 将area对象转换为字典,并保存在列表中
    # area_dict_li = [ {"aid":area.id, "aname":area.name} for area in area_li]
    area_dict_li = [ area.to_dict() for area in area_li]  # 使用模型中定义的对象转为字典的方法

    # 将数据保存到redis中 - 缓存
    # 将数据转换为json字符串
    resp_dict = dict(errno=RET.OK, errmsg="OK", data=area_dict_li)
    resp_json = json.dumps(resp_dict)
    # 将json字符串保存到redis中
    try:
        redis_store.setex("area_info", constants.AREA_INFO_REDIS_CACHE_EXPIRE, resp_json)
    except Exception as e:
        current_app.logger.error(e)

    return resp_json, 200, {"Content-Type":"application/json"}

