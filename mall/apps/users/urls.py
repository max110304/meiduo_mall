from django.conf.urls import url
from . import views
from rest_framework_jwt.views import obtain_jwt_token
urlpatterns = [
    url(r'^usernames/(?P<username>\w{5,20})/count/$',views.RegisterUsernameCountView.as_view(),name='usernamecount'),
    url(r'^phones/(?P<mobile>1[345789]\d{9})/count/$',views.RegisterPhoneCountView.as_view(),name='phonecount'),

    url(r'^$',views.RegisterCreateUserView.as_view()),

    #定义url
    url(r'^auths/', obtain_jwt_token),


]
"""
"token": "

header:     eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.
payload:    eyJ1c2VyX2lkIjo1LCJlbWFpbCI6IiIsInVzZXJuYW1lIjoiaXRjYXN0IiwiZXhwIjoxNTQxNTgyODA1fQ.
signature:  OcJz5BOX5MAalgcn5SjV12a47QFAMGfLGh_3Xs3BopI"
"""