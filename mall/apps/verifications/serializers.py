from rest_framework import serializers
from django_redis import get_redis_connection
# serializers.ModelSerializer
# serializers.Serializer

# 我们数据没有模型 选择serailizer
class RegisterSmscodeSerializer(serializers.Serializer):

    text = serializers.CharField(label='图片验证码',max_length=4,min_length=4,required=True)
    # uuid
    image_code_id = serializers.UUIDField(label='uuid',required=True)
    """
     校验：
        1. 字段类型
        2. 字段选项
        3. 单个字段
        4. 多个字段

        校验图片验证码的时候 需要用到 text和 image_code_id 这2个字段,所以选择 多个字段校验
    """

    def validate(self, attrs):

        # data --> attrs
        # 1 获取用户提交的图片验证码
        text = attrs.get('text')
        image_code_id = attrs.get('image_code_id')

        # 2 获取redis验证吗
        # 2.1 连接redis
        redis_conn = get_redis_connection('code')

        # 2.2 获取redis_text
        redis_text = redis_conn.get('img_%s'%image_code_id)

        # 2.3 判断是否过期
        if redis_text is None:
            raise serializers.ValidationError('图片验证码已过期')

        # 3 比对
        # 2个注意点： redis_text 是bytes类型
        #           大小写问题
        if redis_text.decode().lower() != text.lower():
            raise serializers.ValidationError("图片验证码不一致")


        # 校验完成 需要返回 attrs
        return attrs