from rest_framework.views import APIView

from rest_framework.permissions import IsAdminUser
from app.tokens.tokens import SCMTokenAuthentication
from utils.func import JsonResponse


class RolesAPIView(APIView):
    authentication_classes = (SCMTokenAuthentication, )
    permission_classes = (IsAdminUser,)

    def post(self, request, format=None):
       pass