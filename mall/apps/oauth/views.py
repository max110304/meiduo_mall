from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response

from .serializers import OauthQQUserSerializer
from oauth.utils import generic_access_token

"""
 1. 获取code
 2. 通过code 换取 token
 3. 通过token 换去 openid
"""

"""
用户点击 qq登陆按钮的时候 前段应该发送一个 ajax请求，来获取要跳转的url

这个url 是根据 腾讯的文档来生成的

GET     /oauth/qq/statues/
"""
from rest_framework.views import APIView
from QQLoginTool.QQtool import OAuthQQ
from django.conf import settings
# from mall import settings
class OauthQQURLView(APIView):

    def get(self,request):
        state = '/'

        # 1 创建 oauth对象
        #client_id=None, client_secret=None, redirect_uri=None, state=None
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state=state)

        # 2 调用方法，获取url
        login_url = oauth.get_qq_url()
        # login_url="# login_url = 'https://graph.qq.com/oauth2.0/authorize?response_type=code&redirect_uri=http%3A%2F%2Fwww.meiduo.site%3A8080%2Foauth_callback.html&state=%2F&client_id=101474184'"

        return Response({"login_url":login_url})


"""
前段应该 在用户扫描完成之后,跳转到 http://www.meiduo.site:8080/oauth_callback.html?code=6E2E3F64C34ECFE29222EBC390D29196&state=test
把code 传递给后端,

GET     /oauth/qq/users/?code=xxx

# 1.我们获取到这个code, 通过接口来换去 token
# 2.有了token,就可以换取 oepnid


"""
from rest_framework import status
from .models import OAuthQQUser


class OauthQQUserView(APIView):

    def get(self,request):
        code = request.query_params.get('code')
        if code is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # 1.我们获取到这个code, 通过接口来换去 token
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI)
        access_token = oauth.get_access_token(code)
        # 2.有了token,就可以换取 oepnid
        openid = oauth.get_open_id(access_token)

        # 3 我们需要openid 来进行判断
        # 如果数据库中 有openid 则表明用户已经绑定过
        # 如果数据库中 没有openid 则表明用户没有绑定
        try:
            qquser = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 说明没有绑定过
            """
            1 需要对敏感数据进行处理
            2  数据还需要一个有效期
            """
            #  我们需要对敏感数据进行处理
            openid = generic_access_token(openid)

            return Response({'access_token':openid})


        else:
            # 说明存在, 用户已经绑定过来了,绑定过应该登录
            # 既然是登录,则应该返回token
            # 没有异常 走 else
            from rest_framework_jwt.settings import api_settings

            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(qquser.user)
            token = jwt_encode_handler(payload)

            return Response({
                "user_id":qquser.id,
                "username":qquser.user.username,
                "token":token
            })


    """
    用户点击绑定按钮的时候,前端应该将 手机号,密码,openid,sms_code 发送给后端

    1. 接收数据
    2. 对数据进行校验
        2.1 校验 openid 和sms_code
        2.2 判断手机号
            如果注册过,需要判断 密码是否正确
            如果没有注册过,创建用户
    3. 保存数据
        3.1保存 user 和 openid
    4. 返回响应

    POST

    """
    def post(self,request):

        # 1 接收数据
        data = request.data

        # 2. 对数据进行校验
        #     2.1 校验 openid 和sms_code
        #     2.2 判断手机号
        #         如果注册过,需要判断 密码是否正确
        #         如果没有注册过,创建用户
        serializer = OauthQQUserSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        # 3 保存数据
        qquser = serializer.save()

        # 4 返回响应
        from rest_framework_jwt.settings import api_settings

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(qquser.user)
        token = jwt_encode_handler(payload)

        return Response({
            "user_id": qquser.id,
            "username": qquser.user.username,
            "token": token
        })






# 加密签名
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,BadSignature,SignatureExpired
from django.conf import settings

# 1 创建序列化器
# secret_key    秘钥,一般使用工程的 SECRET_KEY
# expires_in=None 有效期 单位秒
serializer = Serializer(settings.SECRET_KEY,3600)

# 2 组织 加密数据
data = {'openid':'12345679'}
# 3 进行加密数据
token = serializer.dumps(data)

"""
eyJhbGciOiJIUzI1NiIsImV4cCI6MTU0MTY4MTU0MiwiaWF0IjoxNTQxNjc3OTQyfQ.
eyJvcGVuaWQiOiIxMjM0NTY3OSJ9.
Ni-gLgSUGKSu_4kqdiP0HkkAmw7et1OZlDHfYp_-Aqo
"""

# 4 对数据进行解密
serializer.loads(token)

# 5 有效期
serializer = Serializer(settings.SECRET_KEY,1)
