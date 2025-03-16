from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render
import pathlib
from .auth_utlis import *
from .serializers import *


templates_dir = pathlib.Path(__file__).resolve().parent / "templates" / "backend_main"






class Process_browser_view(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]
    
    def get(self, request):
        status_, resp_ = auth_user(request)
        if status_:
            return render(request, f'{templates_dir}/process_browser.html')
        else:
            return redirect('/sign-in/') 



@api_view(['GET'])
@permission_classes([AllowAny]) 
def Process_API(request):
    
    try:
        pass
        #1. Get processes list
        #2. Serialize them
        #3. Send serialized data
        
        #instance = Document_object.objects.filter(owner__id=request.user.id)
        #serializer = DocumentSerializer(instance, many=True)
        #return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"ERROR":"Not implemented"}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"ERROR":f"{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



class Snapshot_browser_view(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]
    
    def get(self, request):
        status_, resp_ = auth_user(request)
        if status_:
            return render(request, f'{templates_dir}/snapshot_browser.html')
        else:
            return redirect('/sign-in/') 

   


class Kill_Log_browser_view(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]
    
    def get(self, request):
        status_, resp_ = auth_user(request)
        if status_:
            return render(request, f'{templates_dir}/killlog_browser.html')
        else:
            return redirect('/sign-in/') 
    


###########################################################################
#Auth methods

 

@api_view(['GET'])
@permission_classes([AllowAny])
def Register_view(request):
    #TODO:
    #1.check if has valid cookies, if yes -> redirect    
    
    return render(request, f'{templates_dir}/sign_up.html')
   


@api_view(['POST'])
@permission_classes([AllowAny]) 
def Register_API(request):
    try: 
        serializer_ = UserSerializer(data=request.data)
        if serializer_.is_valid():
            serializer_.save()
            return Response({"OK": "User created sucesfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"ERROR": f"{serializer_.errors}"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"ERROR": f"{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
@permission_classes([AllowAny])
def Login_view(request):
    #TODO:
    #1.check if has valid cookies, if yes -> redirect    
    
    return render(request, f'{templates_dir}/sign_in.html')



@api_view(['POST'])
@permission_classes([AllowAny])
def Login_API(request):
    #TODO:
    #1.Return some html for frontend on fail
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        
        if user:
            tokens = get_tokens_for_user(user)  # Generate JWT
            response = JsonResponse({"message": "Login successful"})
            response.set_cookie("access_token", tokens["access"], httponly=True, samesite="Strict", secure=True)
            response.set_cookie("refresh_token", tokens["refresh"], httponly=True, samesite="Strict", secure=True)
            response["HX-Redirect"] = "/proc-browser/"
            return response
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)
