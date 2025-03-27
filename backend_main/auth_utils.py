from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
import jwt




from rest_framework.exceptions import AuthenticationFailed

from rest_framework.response import Response

from rest_framework.views import exception_handler
from django.shortcuts import redirect
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, PermissionDenied
import pathlib
templates_dir = pathlib.Path(__file__).resolve().parent / "templates" / "backend_main"









def custom_exception_handler(exc, context):
    request = context.get('request')

    if isinstance(exc, (AuthenticationFailed, NotAuthenticated,PermissionDenied)):
        return redirect("/sign-in/")
      


    response = exception_handler(exc, context)
    if response is None:
        return Response({"error": "An unexpected error occurred"}, status=500)
    return response




def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def auth_user(request):
    # Get acess token from cookies
    token = request.COOKIES.get("access_token")

    if not token:
        return False, "No token provided"

    try:
        decoded_token = AccessToken(token)

        # TODO: check if token blacklisted!
        # RefreshToken(token).check_blacklist()

        return True, decoded_token["user_id"]

    except Exception as e:
        if isinstance(e, jwt.ExpiredSignatureError):
            return False, "Token expired"
        elif isinstance(e, jwt.InvalidTokenError):
            return False, "Invalid token"
        elif TokenError:
            return False, "Token blacklisted"
        else:
            return False, "Authentication failed"


def ban_token(request):
    refresh_token = request.COOKIES.get("refresh_token")

    if not refresh_token:
        return False, "No token provided"

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return True, "Token blacklisted"
    except Exception as e:
        return False, f"{e}"
