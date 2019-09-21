# coding=utf-8

from CCPRestSDK import REST

# 主帐号
# accountSid= '您的主帐号'
accountSid = '8aaf07086d05d00c016d527db89133b0'

# 主帐号Token
# accountToken= '您的主帐号Token'
accountToken = 'a9ca3f84696f438098761dd179c96672'

# 应用Id
# appId='您的应用ID'
appId = '8aaf07086d05d00c016d527db8e333b7'

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'

# 请求端口
serverPort = '8883'

# REST版本号
softVersion = '2013-12-26'


# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为列表 例如：['12','34']，如不需替换请填 ''
# @param $tempId 模板Id

class CCP(object):
    """自己封装的发送短信的辅助类"""
    # 用来保存对象的属性
    instance = None

    def __new__(cls):
        # 判断CCP类有没有创建过对象,如果没有创建一个对象,把那个保存下来
        if cls.instance is None:
            obj = super(CCP, cls).__new__(cls)

            # 初始化REST SDK
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)

            cls.instance = obj

        # 如果有对象,则将保存的对象直接返回
        return cls.instance

    def send_Template_SMS(self, to, datas, tempId):
        result = self.rest.sendTemplateSMS(to, datas, tempId)
        # for k, v in result.iteritems():
        #     if k == 'templateSMS':
        #         for k, s in v.iteritems():
        #             print '%s:%s' % (k, s)
        #     else:
        #         print '%s:%s' % (k, v)
        status_code = result.get("statusCode")
        if status_code == "000000":
            # 表示发送短信成功
            return 0
        else:  # 发送短信失败
            return -1


# def sendTemplateSMS(to,datas,tempId):
#
#
#     #初始化REST SDK
#     rest = REST(serverIP,serverPort,softVersion)
#     rest.setAccount(accountSid,accountToken)
#     rest.setAppId(appId)
#
#     result = rest.sendTemplateSMS(to,datas,tempId)
#     for k,v in result.iteritems():
#
#         if k=='templateSMS' :
#                 for k,s in v.iteritems():
#                     print '%s:%s' % (k, s)
#         else:
#             print '%s:%s' % (k, v)


# sendTemplateSMS(手机号码,内容数据,模板Id)


if __name__ == '__main__':
    ccp = CCP()
    res = ccp.send_Template_SMS("18103763930",["1234","5"],1)
    print res

    # smsMessageSid:a303ab10bf1f4a0cabb6a0a47bbfdc26
    # dateCreated:20190921171556
    # statusCode:000000