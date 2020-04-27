from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from utils.func import JsonResponse
from rest_framework.authtoken.views import AuthTokenSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate

import cfg

from app.permission.token import TOKENEXPIRELRUCACHE


class AutoTokenCreateAPI(ObtainAuthToken):
    def post(self, request, format=None):

        jd = request.data
        email = jd['email']
        passwd = jd['password']
        u = authenticate(email=email, password=passwd)
        if not u:
            return JsonResponse(code=403, msg="验证失败,禁止获取Token")

        if not u.is_active:
            return JsonResponse(code=403, msg="用户未激活,禁止获取Token")

        data = {'uid':u.pk, 'email': u.email, 'access_token': ''}
        token, _ = Token.objects.get_or_create(user=u)
        if not token:
            return JsonResponse(code=400, data=data, msg="创建Token失败")

        data['access_token'] = token.key
        TOKENEXPIRELRUCACHE.add(key=token.key, value=token, expires=cfg.API_TOKEN['expire'])
        return JsonResponse(code=200, data=data, msg="success")
