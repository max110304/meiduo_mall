from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response

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

"""
当用户点击 获取短信验证码的时候 前端应该将 手机号 短信验证码和uuid（image_code_id）发送给后端

1. 接收前端数据
2. 校验数据
3. 先生成短信
4. 发送短信
5. 返回响应


GET         /verifications/sms_codes/ mobile/uuid/text/
GET         /verifications/sms_codes/?mobile=xxx&uuid=xxx&text=xxx

GET         /verifications/sms_codes/(?P<mobile>1[3-9]\d{9})/?uuid=xxx&text=xxx  选择这个
"""
# APIView
#GenericAPIView             列表,详情视图做了通用的支持,一般和一个多个mixin配合使用
#ListAPIView,RetreveAPIView
from .serializers import RegisterSmscodeSerializer
from libs.yuntongxun.sms import CCP
class RegisterSmscodeView(APIView):
    # verifications/smscodes/(?P<mobile>1[345789]\d{9})/?text=xxxx & image_code_id=xxxx
    def get(self,request,mobile):

        # 1.接收前端数据
        params = request.query_params

        # 2. 校验数据

        # text = params.get('text')
        # image_code_id = params.get('dd')
        #
        # if not all([text,image_code_id]):
        #     pass
        # 校验
        serializer = RegisterSmscodeSerializer(data=params)
        # 调用 is_valid 才会校验
        serializer.is_valid(raise_exception=True)

        # 3. 先生成短信
        from random import randint
        sms_code = "%06d"%randint(0,999999)
        # 4. 保存短信，发送短信
        redis_conn = get_redis_connection('code')
        redis_conn.setex('sms_%s'%mobile,300,sms_code)

        # CCP().send_template_sms(mobile,[sms_code,5],1)
        from celery_tasks.sms.tasks import send_sms_code
        # delay 的参数和send_sms_code 任务的参数是对应的
        send_sms_code.delay(mobile,sms_code)
        # 5. 返回响应
        return Response({'msg':'OK'})

