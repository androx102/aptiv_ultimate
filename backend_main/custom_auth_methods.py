from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import UserObject
import jwt



class Custom_jwt_cookie_auth(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('access_token')

        if not token:
            return None  
        
        try:
            decoded_token = AccessToken(token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('JWT has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid JWT')

        try:
            
            user = UserObject.objects.get(id=decoded_token["user_id"])
        except UserObject.DoesNotExist:
            raise AuthenticationFailed('User not found')

        return (user, None)