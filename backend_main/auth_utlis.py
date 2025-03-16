
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings




# Generate JWT tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
    
def auth_user(request):
    token = request.COOKIES.get("access_token")

    if not token:
        return False, "No token provided"

    try:
        decoded_token = jwt.decode(token, settings.SIMPLE_JWT["SIGNING_KEY"], algorithms=["HS256"])
        return True, decoded_token['user_id']
    except jwt.ExpiredSignatureError:
        return False, "Token expired"
    except jwt.InvalidTokenError:
        return False, "Invalid token"