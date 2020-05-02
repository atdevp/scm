from app.menu.models import MenuModel
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from app.tokens.tokens import SCMTokenAuthentication
from utils.func import JsonResponse


class MenuListAPI(APIView):
    """
    获取当前用户的菜单权限
    """

    permission_classes = (IsAuthenticated, )
    authentication_classes = (SCMTokenAuthentication, )

    def get(self, request, format=None):
        menus = []
        qs = MenuModel.objects.all()
        if not qs:
            return JsonResponse(code=404, msg="Not Find MenuList")

   
        for i in qs.filter(parent_id=0):
            parent = {
                'id': i.id,
                'name': i.name,
                'show_name': i.show_name,
                'url': i.url,
                'icon': i.icon
            }
            sub_menus = []
            for j in qs.filter(parent_id=i.id):
                child = {
                    'id': j.id,
                    'name': j.name,
                    'show_name': j.show_name,
                    'url': j.url,
                    'icon': j.icon
                }
                sub_menus.append(child)
            parent['children'] = sub_menus

            menus.append(parent)

        return JsonResponse(code=200, data=menus, msg="success")


        
