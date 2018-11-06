import re

from django_redis import get_redis_connection
from rest_framework import serializers
from users.models import User
# serializers.ModelSerializer
# serializers.Serializer

# 数据入库 选择ModelSerializer 肯定有 模型
class RegisterCreateUserSerializer(serializers.ModelSerializer):

    """
    6个参数(username,password,password2,mobile,sms_code,allow)

    """
    sms_code = serializers.CharField(label='短信验证码',min_length=6,max_length=6,required=True)
    password2 = serializers.CharField(label='确认密码',required=True)
    allow = serializers.CharField(label='同意协议',required=True)
    class Meta:
        model = User
        fields = ['username','password','mobile','sms_code','password2','allow']



    #  1 手机号校验，密码一致，短信校验，是否同意
    #     手机号 就是规则 单个字段
    #       密码一致，短信校验 多个字段
    def validata_mobile(self,value):

        if not re.match('1[3-9]\d{9}',value):
            raise serializers.ValidationError('手机号不满足规则')
        # 校验之后 返回
        return value

    def validated_allow(self,value):

        if value == 'false':
            raise serializers.ValidationError('您未同意协议')

        return value

    def validate(self, attrs):

        # 密码一致
        password = attrs.get('password')
        password2 = attrs.get('password2')
        mobile = attrs.get('mobile')
        sms_code = attrs.get('sms_code')

        if password != password2:
            raise serializers.ValidationError('密码不一致')

        #2 短信
        redis_conn = get_redis_connection('code')

        sms_code_redis = redis_conn.get('sms_%s'%mobile)
        if sms_code_redis is None:
            raise serializers.ValidationError('验证码已过期')

        if sms_code_redis.decode() != sms_code:
            raise serializers.ValidationError('验证码错误')

        return attrs