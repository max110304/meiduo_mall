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