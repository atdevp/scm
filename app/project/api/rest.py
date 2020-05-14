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


class ProjectPostBuildAPI(APIView):
    permission_classes = (
        IsAuthenticated,
        IsAdminUser,
    )
    authentication_classes = (SCMTokenAuthentication, )
    throttle_classes = (IPRateThrottle, )

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
        return JsonResponse(
            data={
            "mods": mods,
            "new_tag": nv,
            "type": p.p_type
            },
            code=200,
            msg="success"
        )


class ProjectPostGetCompileCommandAPI(APIView):
    permission_classes = ( IsAuthenticated, IsAdminUser,)
    authentication_classes = (SCMTokenAuthentication, )
    throttle_classes = (IPRateThrottle, )

    def post(self, request, pk, format=None):
        jd = request.data
        pkg_user = request.user.email

        if not isinstance(jd, dict):
            return JsonResponse(code=400, msg="Invalid post body format")

        cmd = ""
        jd['pid'] = pk
        jd['pkg_user'] = pkg_user
        try:
            cmd = gen_pkg_command(jd)
        except Exception as e:
            traceback.print_exc()
            return JsonResponse(code=500, msg=str(e))
        
        print(cmd)

        return JsonResponse(code=200, msg="success", data={"command": cmd})


def gen_pkg_command(arg):

    if not ProjectModel.objects.filter(id=arg['project']).exists():
        raise GeneratePakcageCommandError("project not find")

    p = ProjectModel.objects.get(id=arg['project'])

    version = arg['version'] if arg['scheme'] == "online" else None
    module = arg['module'] if arg['module'] != "no-module" else None 
    info = arg['info'] 

    pro_path = os.path.join(cfg.CICD_CFG['SRC_CODE_PATH'], p.name)

    if not os.path.exists(pro_path):
        g = git.Git(url=p.url)
        g.clone()
        g.checkout(br=arg['branch'])
        g.pull(br=arg['branch'])

    # arg['name'], arg['puser'] = p.name, request.user.email

    # add package record to mysql
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    PackageLogModel.objects.create(project_id=arg['project'],
                                   msg=info,
                                   puser=arg['pkg_user'],
                                   ptime=now,
                                   tag=version,
                                   env=arg['scheme'],
                                   module=module,
                                   br=arg['branch']).save()

    m = mvn.Mvn(name=p.name, ptype=p.p_type)
    pkg_name = m.get_pkg_name(module)

    save_path = get_save_path(arg['scheme'])
    script = os.path.join(BASE_DIR, 'scripts/package.sh')

    cmd = '{0} -p {1} -m {2} -e {3} -v {4} -t {5} -s {6} -c {7}'.format(script, p.name, arg['module'],
                                                   arg['scheme'], arg['version'],
                                                   pkg_name, save_path,
                                                   arg['dependence'])

    return cmd
