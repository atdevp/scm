# -- condig: UTF-8 --*--
import os
import shutil
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import Serializer
import cfg

# delete directory or file on system
def del_resource(d):
    if os.path.exists(d):
        shutil.rmtree(d) if os.path.isdir(d) else os.remove(d)


# define http jsonResponse
class JsonResponse(Response):
    """
    An HttpResponse that allows its data to be rendered into
    arbitrary media types.
    """
    def __init__(self,
                 data="",
                 code=None,
                 msg=None,
                 status=status.HTTP_200_OK,
                 template_name=None,
                 headers=None,
                 exception=False,
                 content_type=None):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.

        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        super().__init__(None, status=status)

        if isinstance(data, Serializer):
            msg = ('You passed a Serializer instance as data, but '
                   'probably meant to pass serialized `.data` or '
                   '`.error`. representation.')
            raise AssertionError(msg)

        self.data = {"code": code, "message": msg, "data": data}
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in headers.items():
                self[name] = value


#
def get_save_path(env):
    if env == 'online':
        return cfg.CICD_CFG['ONLINE_PACKAGE']

    if env == 'develop':
        return cfg.CICD_CFG['DEVELOP_PACKAGE']

    if env == 'stating':
        return cfg.CICD_CFG['STATING_PACKAGE']

# 判断可以是否存在Dict
def isExistInDict(d, key):
    if not isinstance(d, dict):
        return False
    
    if not key:
        return False

    return key in d.keys()

def _update_field(k, v):
    getattr(k)
    setattr(k, v)

def jsonDataUpdateModel(model, jd, pk):
    if not isinstance(jd, dict):
        return
    
    ob = model.objects.get(id=pk)
    for k, v in jd.items():
        setattr(ob, k, v)
    ob.save()
