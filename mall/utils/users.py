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


from django.contrib.auth.backends import ModelBackend
class MobileUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):


        # username 有可能是 手机号 也有可能是 用户名
        # 手机号有一个规则,我们可以根据 手机号的规则来判断 是用户名还是手机号

        # 1 根据 username 查询用户信息
        try:
            if re.match('1[3-9]\d{9}',username):
                # 手机号
                user = User.objects.get(mobile = username)
            else:
                # 用户名
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

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
        try:
            if re.match('1[3-9]\d{9}', username):
                # 手机号
                user = User.objects.get(mobile=username)
            else:
                # 用户名
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        #2. 校验用户的密码
        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None