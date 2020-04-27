# -- condig:UTF-8 --*--
from rest_framework.views import APIView
from utils.func import JsonResponse, isExistInDict
from utils.func import jsonDataUpdateModel, delLruCache
from rest_framework import generics, status
from django.contrib.auth import authenticate, login, logout
import base64
from app.user.models import UserModel
from app.user.serializers import UserModelSerializer
import time
import pickle
import pylru

from app.permission.token import SCMTokenAuthentication

USERLRUCACHE = pylru.lrucache(size=100)


class UsersListAPI(APIView):

    authentication_classes = (SCMTokenAuthentication,)
    def get(self, request, format=None):
        if "userlist" in USERLRUCACHE.keys():
            data = pickle.loads(USERLRUCACHE['userlist'])
            return JsonResponse(code=200, msg="success", data=data)

        us = UserModel.objects.all()
        sz = UserModelSerializer(us, many=True)
        USERLRUCACHE['userlist'] = pickle.dumps(sz.data)
        return JsonResponse(code=200, msg="success", data=sz.data)


class UsersRegisterAPI(APIView):
    def post(self, request, format=None):
        jd = request.data
        if request.META.get('CONTENT_TYPE') \
            != "application/json":
            return JsonResponse(
                code=400, msg="Http header content-type not application/json")

        if not isinstance(jd, dict):
            return JsonResponse(code=400, msg="Post body not json format")

        if not isExistInDict(jd, "username"):
            return JsonResponse(code=400, msg="缺少usernmae参数")

        if not isExistInDict(jd, "passwd"):
            return JsonResponse(code=400, msg="缺少passwd参数")

        username, passwd = jd['username'], jd['passwd']
        email, mobile = jd['email'], jd['mobile']

        if username == "" or passwd == "" or \
            email == "" or mobile == "":
            return JsonResponse(code=400, msg="字段不能为空")

        if UserModel.objects.filter(username=username).exists():
            return JsonResponse(code=400, msg="用户名{0}已不存".format(username))

        if UserModel.objects.filter(email=email).exists():
            return JsonResponse(code=400, msg="邮箱{0}已不存".format(email))

        if UserModel.objects.filter(mobile=mobile).exists():
            return JsonResponse(code=400, msg="手机号{0}已不存".format(mobile))

        u = UserModel.objects.create_user(
            username=username,
            email=email,
            password=base64.b64decode(passwd).decode('utf-8'),
            mobile=mobile)
        print(u.save())

        sz = UserModelSerializer(jd)
        delLruCache(USERLRUCACHE, 'userlist')
        return JsonResponse(code=200, msg="Register success", data=sz.data)


class UserLoginAPI(APIView):
    def post(self, request, format=None):
        if request.META.get('CONTENT_TYPE') \
            != "application/json":
            return JsonResponse(
                code=400, msg="Http header content-type not application/json")

        jd = request.data
        if not isinstance(jd, dict):
            return JsonResponse(code=400, msg="Post body not json format")

        email, passwd = jd['email'], jd['password']
        u = authenticate(email=email, password=passwd)
        if not u:
            return JsonResponse(code=403, msg="验证失败，禁止登录")
        if not u.is_active:
            return JsonResponse(code=403, msg="用户未激活")
        
        login(request, u)
        request.session['is_login'] = True
        return JsonResponse(code=200, msg="用户登录成功")


class UserLogoutAPI(APIView):
    def get(self, request, format=None):
        logout(request)
        request.session['is_login'] = False
        return JsonResponse(code=200, msg="退出登录成功")



class UserDetailListAPI(APIView):
    def get(self, request, pk, format=None):
        if not UserModel.objects.filter(id=pk).exists():
            return JsonResponse(code=400, msg="User not find")

        u = UserModel.objects.get(id=pk)
        sz = UserModelSerializer(u)
        return JsonResponse(code=200, msg="", data=sz.data)


class UserDetailUpdateAPI(APIView):
    def post(self, request, pk, format=None):
        if not UserModel.objects.filter(id=pk).exists():
            return JsonResponse(code=400, msg="User not find")

        jd = request.data

        if isExistInDict(jd, "username"):
            return JsonResponse(code=403, msg="username不可修改")

        if isExistInDict(jd, "email"):
            return JsonResponse(code=403, msg="email不可修改")

        try:
            jsonDataUpdateModel(UserModel, jd, pk)
        except Exception as e:
            return JsonResponse(code=500, msg=str(e))

        delLruCache(USERLRUCACHE, 'userlist')
        return JsonResponse(code=200, msg="success")


class UserDetailDeleteAPI(APIView):
    def get(self, request, pk, format=None):
        if not UserModel.objects.filter(id=pk).exists():
            return JsonResponse(code=400, msg="User not find")

        UserModel.objects.filter(id=pk).delete()
        delLruCache(USERLRUCACHE, 'userlist')
        return JsonResponse(code=200, msg="success")
