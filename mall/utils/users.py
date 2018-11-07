
def jwt_response_payload_handler(token, user=None, request=None):

    # jwt 的token
    #  user 已经认证之后的用户信息
    return {
        'token': token,
        'username':user.username,
        'user_id':user.id
    }