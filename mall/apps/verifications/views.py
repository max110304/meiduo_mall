from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

"""
一.  先把需求写下来
二.  根据需求 确定采用那种请求方式
三.  确定视图    进行编码


1  前段需要发送给我一个 uuid  这个时候我们接收到uuid之后生成一个图片 给前段
2  接收前端提供的uuid
3   生成图片验证码，保存 图片验证码的数据
4   返回响应

GET              /verifications/imagecodes/(?P<image_code_id>.+)/

"""
# APIView
#GenericAPIView             列表,详情视图做了通用的支持,一般和一个多个mixin配合使用
#ListAPIView,RetreveAPIView

from rest_framework.views import APIView
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
class RegisterImageCodeView(APIView):

    def get(self,request,image_code_id):

        #  1  生成图片验证码，
        text,image = captcha.generate_captcha()
        # 2     保存 图片验证码的数据
        redis_conn = get_redis_connection('code')
        from . import constant
        redis_conn.setex('img_%s'%image_code_id,constant.IMAGE_CODE_EXPIRE_TIME,text)
        # 3   返回响应
        # return HttpResponse(image,content_type='application/json')
        return HttpResponse(image,content_type='image/jpeg')
