# -*- coding:utf-8 -*-
# @Desc : 
# @Author : Administrator
# @Date : 2019-09-23 19:18

from qiniu import Auth, put_data, etag
import qiniu.config

# Access Key 和 Secret Key (在个人用户中心的秘钥管理中查找)
access_key = 'K8-aPB6c05hMs5VHsexXuhusv0yV_9E3E1iJpVfA'
secret_key = 'mTo2c-nm2IAg-6MKd0pWfdXPz-PCG7KZKQxUuu9r'


def storage(file_data):
    """
    上传图片文件到七牛
    :param file_data: 要上传的文件数据
    :return:
    """

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间名称("对象存储"中创建的存储空间名称)
    bucket_name = 'cd-python-ihome'

    # 上传后保存的文件名(可选)
    # key = 'my-python-logo.png'

    # 生成上传Token,可以指定过期时间等
    # 因为上传后保存的文件名字key没有指定,所以此处key值设置为None
    # token = q.upload_token(bucket_name, key, 3600)
    token = q.upload_token(bucket_name, None, 3600)

    # 要上传文件的本地路径
    # localfile = './sync/bbb.jpg'
    # ret, info = put_file(token, key, localfile)  # tiken 文件名字 文件
    ret, info = put_data(token, None, file_data)  # token 文件名字 文件二进制数据

    # 注: 返回值info是一个对象,包含状态码status_code:200(表示上传成功)
    # 注: 返回值ret是一个字典,hash:哈希计算结果值和key:上传后的文件名字,因为此前未指定上传文件的名字,所以上传后的文件名字使用的是哈希计算结果值

    print(info)
    # assert ret['key'] == key
    # assert ret['hash'] == etag(localfile)

if __name__ == '__main__':
    with open("iHome/Note/数据库模型关系.png","rb") as ft:
        file_data = ft.read()
        storage(file_data)

