from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response

# from apps.users.models import User  # 错误的
from users.models import User   # 这是pycharm 认为的错误
"""
一, 确定需求
二,  确定采用哪种请求方式 和 url
三,  实现


1.前端发送一个ajax请求,给后端,参数是 用户名

# 2.后端接收用户名
# 3.查询校验是否重复
# 4.返回响应

GET     /users/usernames/(?P<username>\w{5,20})/count/



"""
# APIView
# GenericAPIView                    列表,详情通用支持,一般和mixin配合使用
# ListAPIView,RetrieveAPIView
from rest_framework.views import APIView
"""
1.前段传递过来的数据 已经在 url中校验过了
2. 我们也不需要 序列化器
"""

class RegisterUsernameCountView(APIView):

    def get(self,request,username):

        # 2.后端接收用户名
        # username
        # 3.查询校验是否重复
        # count = 0 表示没有注册
        # count = 1 表示注册
        count = User.objects.filter(username=username).count()

        # 4 返回响应
        return Response({'count':count,'username':username})

"""
1.前端发送一个ajax请求,给后端,参数是 手机号
# 2.后端接收手机号
# 3.查询校验是否重复
# 4.返回响应

"""
class RegisterPhoneCountView(APIView):

    def get(self,request,mobile):

        # 查询校验是否重复
        count = User.objects.filter(mobile=mobile).count()

        # 返回响应
        return Response({'count':count,'moblie':mobile})


"""
前段应该 将6个参数(username,password,password2,mobile,sms_code,allow) 传递给后端

1 接收前端提交的数据
2 校验数据
3 数据入库
4 返回响应

POST        users/


"""


# APIView
# GenericAPIView                    列表,详情通用支持,一般和mixin配合使用
# CreateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import CreateAPIView
from .serailizers import RegisterCreateUserSerializer
class RegisterCreateUserView(APIView):

    def post(self,request):
        # 1 接收前端提交的数据

        # username = request.form.get('username')
        data = request.data
        # 2 校验数据

        # if not all([]):
        #     pass
        #
        # pass

        serializer = RegisterCreateUserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        # 3 数据入库
        serializer.save()
        # 4 返回响应
        return  Response(serializer.data)

