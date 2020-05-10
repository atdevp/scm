from rest_framework.views import APIView
from rest_framework import generics, status
from app.project.serializers import ProjectSerializer, PackageLogsSerializer
from app.project.models import ProjectModel, PackageLogModel
from app.project.models import get_new_tag
from rest_framework import status
from utils.ci import git
from utils.cd import mvn
from utils.func import del_resource, JsonResponse, get_save_path
from utils.func import jsonDataUpdateModel
from django.db import transaction, DatabaseError
from utils.exceptions import GeneratePakcageCommandError
from scm.settings import BASE_DIR
from app.tokens.tokens import SCMTokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from utils.throttle import IPRateThrottle
from utils.pagination import MyPagination
from rest_framework import filters
import traceback
import time
import cfg
import os


class ProjectList(APIView):
    permission_classes = (
        IsAuthenticated,
        IsAdminUser,
    )
    authentication_classes = (SCMTokenAuthentication, )
    throttle_classes = (IPRateThrottle, )

    def get(self, request, format=None):
        pagination_class = MyPagination()
        search_class = filters.SearchFilter()

        projects = ProjectModel.objects.all().order_by('id')
        self.search_fields = ['url', 'name', 'p_type']

        search_query = search_class.filter_queryset(request, projects, self)
        page_query = pagination_class.paginate_queryset(queryset=search_query,
                                                        request=request,
                                                        view=self)

        sz = ProjectSerializer(page_query, many=True)
        res = pagination_class.get_paginated_response(sz.data)

        return JsonResponse(data=res, code=200, msg="success")

    def post(self, request, format=None):
        jd = request.data
        if not isinstance(jd, dict):
            return JsonResponse(code=400, msg="Invalid post body format")

        url, func, p_type = jd['url'], jd['func'], jd['type']
        

        name = url.split("/")[-1].split(".")[0] if url else None

        code_path = cfg.CICD_CFG['SRC_CODE_PATH']
        if os.path.exists(os.path.join(code_path, name)) and \
                ProjectModel.objects.filter(name=name).exists():
            return JsonResponse(code=201, msg="success", data=jd)

        try:
            p = ProjectModel.objects.create(name=name,
                                            url=url,
                                            p_type=p_type,
                                            creator=request.user.email,
                                            func=func)
            p.save()
        except DatabaseError as e:
            return JsonResponse(code=500, msg=str(e))

        try:
            g = git.Git(url)
            g.clone()
        except git.CloneError as e:
            ProjectModel.objects.filter(name=name, url=url,
                                        p_type=p_type).delete()
            return JsonResponse(code=500, msg=str(e))

        return JsonResponse(code=201, msg="success", data=jd)


class ProjectDetail(APIView):
    def get(self, request, pk, format=None):
        try:
            p = ProjectModel.objects.get(id=pk)
            sz = ProjectSerializer(p)
        except Exception as e:
            return JsonResponse(code=500, msg=str(e))

        return JsonResponse(data=sz.data, code=200, msg="success")

    def put(self, request, pk, format=None):
        try:
            jsonDataUpdateModel(ProjectModel, jd, pk)
        except Exception as e:
            return JsonResponse(code=500, msg=str(e))

        return JsonResponse(code=200, msg="success")

    def delete(self, request, pk, format=None):
        try:
            p = ProjectModel.objects.get(id=pk)
            d = os.path.join(cfg.CICD_CFG['SRC_CODE_PATH'], p.name)
            del_resource(d)
            p.delete()
        except Exception as e:
            return JsonResponse(code=500, msg=str(e))

        return JsonResponse(code=200, msg="success")


class ProjectPostBuild(APIView):
    def get(self, request, pk, format=None):
        mods = []

        p = ProjectModel.objects.get(id=pk)
        try:
            m = mvn.Mvn(p.name, p.p_type)
            mods = m.get_mods()
        except Exception as e:
            traceback.print_exc()
            return JsonResponse(code=500, msg=str(e))

        nv = get_new_tag(pk)
        return JsonResponse(data={
            "mods": mods,
            "new_tag": nv,
            "type": p.p_type
        },
                            code=200,
                            msg="success")

    def post(self, request, pk, format=None):
        d = request.data
        pkg_user = "request.user.email"

        cmd = ""
        d['pid'] = pk
        try:
            cmd = gen_pkg_command(d)
        except Exception as e:
            traceback.print_exc()
            return JsonResponse(code=500, msg=str(e))

        return JsonResponse(code=200, msg="success", data=cmd)


def gen_pkg_command(arg):

    if not ProjectModel.objects.filter(id=arg['pid']).exists():
        raise GeneratePakcageCommandError("project not find")

    p = ProjectModel.objects.get(id=arg['pid'])

    tag = arg['pkg_tag'] if arg['pkg_env'] == "online" else None
    mod_name = arg['pkg_mod'] if 'pkg_mod' in arg.keys() else None
    pkg_msg = arg['pkg_msg'] if 'pkg_msg' in arg.keys() else None

    pro_path = os.path.join(cfg.CICD_CFG['SRC_CODE_PATH'], p.name)

    if not os.path.exists(pro_path):
        g = git.Git(url=p.url)
        g.clone()
        g.checkout(br=arg['pkg_br'])
        g.pull(br=arg['pkg_br'])

    arg['name'], arg['puser'] = p.name, 'request.user.email'

    # add package record to mysql
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    PackageLogModel.objects.create(project_id=arg['pid'],
                                   msg=pkg_msg,
                                   puser=arg['puser'],
                                   ptime=now,
                                   tag=tag,
                                   env=arg['pkg_env'],
                                   module=mod_name,
                                   br=arg['pkg_br']).save()

    m = mvn.Mvn(name=p.name, ptype=p.p_type)
    pkg_name = m.get_pkg_name(mod_name)

    save_path = get_save_path(arg['pkg_env'])
    script = os.path.join(BASE_DIR, 'scripts/package.sh')

    cmd = '{0} {1} {2} {3} {4} {5} {6} {7}'.format(script, p.name, mod_name,
                                                   arg['pkg_env'], tag,
                                                   pkg_name, save_path,
                                                   arg['is_or_dependent'])

    return cmd
