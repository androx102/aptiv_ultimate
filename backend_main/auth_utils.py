from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import exception_handler
from django.shortcuts import redirect
from django.conf import settings
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
import pathlib

templates_dir = pathlib.Path(__file__).resolve().parent / "templates" / "backend_main"
RED = '\033[31m'
RESET = '\033[0m'

def custom_exception_handler(exc, context):
    if isinstance(exc, (AuthenticationFailed, NotAuthenticated, PermissionDenied)):
        return redirect("/sign-in/")
    
    if settings.DEBUG == True:
        print(f"{RED}####### WARNING! CRITICAL ERROR! ######{RESET}\n")
        print(f"{RED}Context:{RESET} {context}\n {RED}Error:{RESET}{exc}\n")
        print(f"{RED}#######################################{RESET}\n")
        
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
