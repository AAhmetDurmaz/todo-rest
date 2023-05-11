import jwt
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from authentication.models import User
from todo.settings import SECRET_KEY, ENCRYPTION_ALGORITHM
from rest_framework import exceptions
import jwt


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = get_authorization_header(request)
        auth_data = auth_header.decode('utf-8')
        auth_token = auth_data.split(" ")
        if len(auth_token) != 2:
            raise exceptions.AuthenticationFailed('Token not valid')
        token = auth_token[1]

        try:
            payload = jwt.decode(
                token, SECRET_KEY, algorithms=ENCRYPTION_ALGORITHM)  # type: ignore
            username = payload['username']
            user = User.objects.get(username=username)
            return (user, token)

        except jwt.ExpiredSignatureError as ex:
            raise exceptions.AuthenticationFailed('Token has expired.')
        except jwt.DecodeError as ex:
            raise exceptions.AuthenticationFailed('Invalid Token')
        except User.DoesNotExist as no_user:
            raise exceptions.AuthenticationFailed('Invalid token.')

        return super().authenticate(request)
