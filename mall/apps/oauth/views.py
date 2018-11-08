from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response


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
        state = 'test'

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
            return Response({'openid':openid})
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
                "userid":qquser.id,
                "username":qquser.username,
                "token":token
            })
