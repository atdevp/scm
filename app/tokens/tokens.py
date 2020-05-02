# 自定义token验证

from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions, HTTP_HEADER_ENCODING
from rest_framework import status
from utils.init import RedisPool
import pickle


class AuthenticationFailed(exceptions.APIException):
    status_code = status.HTTP_200_OK
    default_detail = {'code': 401, 'message': 'Invalid token.', 'data': ''}
    default_code = 'authentication_failed'

def get_authorization_header(request):

    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, str):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth

class SCMTokenAuthentication(TokenAuthentication):

    keyword = 'Token'
    model = None

    def get_model(self):
        if self.model is not None:
            return self.model
        from rest_framework.authtoken.models import Token
        return Token

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            raise AuthenticationFailed('Invalid token header. No credentials provided.')

        if len(auth) == 1:
            raise AuthenticationFailed('Invalid token header. No credentials provided.')
        elif len(auth) > 2:
            raise AuthenticationFailed('Invalid token header. Token string should not contain spaces.')

        try:
            token = auth[1].decode()
        except UnicodeError:
            raise AuthenticationFailed('Invalid token header. Token string should not contain invalid characters.')

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):

        token = None
        token = RedisPool.get(key)
        if token:
            nt = pickle.loads(token)
            return (nt.user, nt.key)

        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted.')

        return (token.user, token)

    def authenticate_header(self, request):
        return self.keyword