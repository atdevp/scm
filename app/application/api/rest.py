# --*-- coding: UTF-8 --*--
from rest_framework.views import APIView
from app.tokens.tokens import SCMTokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from utils.throttle import IPRateThrottle
from utils.pagination import MyPagination
from app.application.models import ApplicationModel
from app.project.models import ProjectModel
from utils.func import JsonResponse
from rest_framework import filters
from app.application.serializers import ApplicationSerializer


class ApplicationListAPI(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser, )
    authentication_classes = (SCMTokenAuthentication, )
    throttle_classes = (IPRateThrottle, )

    def get(self, request, format=None):


        apps = ApplicationModel.objects.all().order_by('id')
        self.search_fields = ['app', 'module', 'port', 'scheme', 'port']
        
        pagination_class = MyPagination()
        search_class = filters.SearchFilter()

        search_query = search_class.filter_queryset(request, apps, self)
        page_query = pagination_class.paginate_queryset(queryset=search_query,
                                                        request=request,
                                                        view=self)

        sz = ApplicationSerializer(page_query, many=True)
        res = pagination_class.get_paginated_response(sz.data)

        return JsonResponse(data=res, code=200, msg="success")


class ApplicationCreateAPI(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser, )
    authentication_classes = (SCMTokenAuthentication, )
    throttle_classes = (IPRateThrottle, )
    
    def _save(self, jd):
        flag = "success"
        try:
            app = ApplicationModel.objects.create(
                app=jd['app'],
                pro_id=ProjectModel.objects.get(id=jd['pro_id']),
                module=jd['module'],
                scheme=jd['scheme'],
                main_class=jd['main_class'],
                main_args=jd['main_args'],
                jvm_args=jd['jvm_args'],
                port=jd['port']
            )
        
            app.save()
        except Exception as e:
            flag = str(e)
        
        return flag

    def post(self, request, format=None):
        jd = request.data

        if not isinstance(jd, dict):
            return JsonResponse(code=400, msg="Content-Type格式非application/json")

        lists = ['app', 'pro_id', 'module', 'scheme', 'main_class', 'main_args', 'jvm_args', 'port']
        if sorted(lists) != sorted(list(jd.keys())):
            return JsonResponse(code=400, msg="请求参数名错误")
        

        if ApplicationModel.objects.filter(app=jd['app'], pro_id=jd['pro_id']).exists():
            return JsonResponse(code=403, msg="应用已存在，禁止创建")
        
        save_msg = self._save(jd)
        if save_msg != "success":
            return JsonResponse(code=500, msg=save_msg)
        
        return JsonResponse(code=201, msg="创建成功", data=jd)

        
