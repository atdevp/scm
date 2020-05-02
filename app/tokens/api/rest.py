from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from utils.func import JsonResponse
from rest_framework.authtoken.views import AuthTokenSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from utils.init import RedisPool
from rest_framework.views import APIView

import cfg
import logging
import pickle

logger = logging.getLogger('scm')


class TokenCreateAPI(ObtainAuthToken):
    def post(self, request, format=None):

        jd = request.data
        email = jd['email']
        passwd = jd['password']
        u = authenticate(email=email, password=passwd)
        if not u:
            return JsonResponse(code=403, msg="验证失败,禁止获取Token")

        if not u.is_active:
            return JsonResponse(code=403, msg="用户未激活,禁止获取Token")

        data = {'uid': u.pk, 'email': u.email, 'access_token': ''}

        token, _ = Token.objects.get_or_create(user=u)
        if not token:
            return JsonResponse(code=400, data=data, msg="创建Token失败")

        data['access_token'] = token.key
        RedisPool.set(name=u.pk,
                      value=pickle.dumps(token),
                      ex=cfg.API_TOKEN['expire_time'])

        return JsonResponse(code=200, data=data, msg="success")


class TokenGetAPI(APIView):
    def post(self, request, format=None):
        jd = request.data
        email = jd['email']
        passwd = jd['password']
        u = authenticate(email=email, password=passwd)
        if not u:
            return JsonResponse(code=403, msg="验证失败,禁止获取Token")

        if not u.is_active:
            return JsonResponse(code=403, msg="用户未激活,禁止获取Token")

        data = {'uid': u.pk, 'email': u.email, 'access_token': ''}

        if RedisPool:
            token = RedisPool.get(u.pk)
            if token:
                logger.info(
                    'Get token from redis for user_id: {0} successfully'.
                    format(u.pk))
                data['access_token'] = pickle.loads(token).key
                return JsonResponse(code=200, data=data, msg="success")

        token = Token.objects.filter(user_id=u.pk).get()
        if not token:
            return JsonResponse(code=404, data=data, msg="用户未生成token")

        data['access_token'] = token.key
        RedisPool.set(name=u.pk,
                      value=pickle.dumps(token),
                      ex=cfg.API_TOKEN['expire_time'])

        return JsonResponse(code=200, data=data, msg="success")
