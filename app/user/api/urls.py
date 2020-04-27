from django.urls import path, re_path
from .rest import UsersListAPI, UsersRegisterAPI, UserDetailListAPI
from .rest import UserDetailUpdateAPI, UserDetailDeleteAPI, UserLoginAPI
from .rest import UserLogoutAPI


urlpatterns = [
    path('register.go', UsersRegisterAPI.as_view()),
    path('login.go', UserLoginAPI.as_view()),
    path('logout.go', UserLogoutAPI.as_view()),
    path('list.go', UsersListAPI.as_view()),
    re_path('^(?P<pk>[0-9]+)/list.go$', UserDetailListAPI.as_view()),
    re_path('^(?P<pk>[0-9]+)/update.go$', UserDetailUpdateAPI.as_view()),
    re_path('^(?P<pk>[0-9]+)/delete.go$', UserDetailDeleteAPI.as_view()),
]