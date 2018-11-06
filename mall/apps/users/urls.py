from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^usernames/(?P<username>\w{5,20})/count/$',views.RegisterUsernameCountView.as_view(),name='usernamecount'),
    url(r'^phones/(?P<mobile>1[345789]\d{9})/count/$',views.RegisterPhoneCountView.as_view(),name='phonecount'),

    url(r'^$',views.RegisterCreateUserView.as_view()),
]