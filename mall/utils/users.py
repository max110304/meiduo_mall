import re

from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):

    # jwt 的token
    #  user 已经认证之后的用户信息
    return {
        'token': token,
        'username':user.username,
        'user_id':user.id
    }


"""

1. 登录是采用的jWT的认证方式, JWT的认证方式是在 rest_framework的基础上做的,也就是说
    JWT 其实就用的 rest_framework 的认证,只不过返回的是 token
    JWT 其实就用的 rest_framework 的认证 , rest_framework 的认证 是根据用户名来判断的

2. 我们需要判断 用户是输入的手机号还是用户名


"""
"""
1. n行代码实现了一个功能(方法) 我们就可以将代码抽取(封装)出去
2. 如果多次出现的代码(第二次出现,就抽取)

 抽取(封装)的思想是:
    1.将要抽取的代码 原封不动的放到一个函数中,函数暂时不需要参数
    2.抽取的代码 哪里有问题 改哪里, 其中的变量,定义为函数的参数
    3.用抽取的函数 替换  原代码,进行测试
"""
def get_user(username):
    try:
        if re.match('1[3-9]\d{9}', username):
            # 手机号
            user = User.objects.get(mobile=username)
        else:
            # 用户名
            user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None
    return user

from django.contrib.auth.backends import ModelBackend
class MobileUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):


        # username 有可能是 手机号 也有可能是 用户名
        # 手机号有一个规则,我们可以根据 手机号的规则来判断 是用户名还是手机号

        # 1 根据 username 查询用户信息

        # try:
        #     if re.match('1[3-9]\d{9}',username):
        #         # 手机号
        #         user = User.objects.get(mobile = username)
        #     else:
        #         # 用户名
        #         user = User.objects.get(username=username)
        # except User.DoesNotExist:
        #     return None

        user = get_user(username)
        # 2 校验用户的密码
        if user is not None and user.check_password(password):
            return user
        return None

class SettingsBackend(object):
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'pbkdf2_sha256$30000$Vo0VlMnkR4Bk$qEvtdyZRWTcOsCnI/oQ7fVOu1XAURIZYoOZ3iq8Dr4M='
    """

    def authenticate(self, request, username=None, password=None):

        # try:
        #     if re.match('1[3-9]\d{9}', username):
        #         # 手机号
        #         user = User.objects.get(mobile=username)
        #     else:
        #         # 用户名
        #         user = User.objects.get(username=username)
        # except User.DoesNotExist:
        #     return None

        user = get_user(username)
        
        #2. 校验用户的密码
        if user is not None and user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None