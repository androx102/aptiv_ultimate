from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
import pathlib
from .auth_utlis import *
from .serializers import *
from .utils import *


templates_dir = pathlib.Path(__file__).resolve().parent / "templates" / "backend_main"
partials_dir = pathlib.Path(__file__).resolve().parent / "templates" / "partials"



@api_view(['GET'])
def index(request):
    status_, resp_ = auth_user(request)
    if status_:
        return render(request, f'{templates_dir}/index.html')
    else:
        return render(request, f'{templates_dir}/index.html',{'require_login': True})
    
    

class Process_browser_view(APIView):    
    def get(self, request):
        status_, resp_ = auth_user(request)
        if status_:
            try:
                processes = get_process_info()
                if request.headers.get('HX-Request') == 'true':
                    return render(request, f'{partials_dir}/proc_table.html', {'processes': processes})
                else:
                    return render(request, f'{templates_dir}/proc-browser.html', {'processes': processes})
                           
            except Exception as e:
                return Response({"ERROR":f"{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        else:
            return redirect('/sign-in/') 


@api_view(['GET'])
def Process_API_snap(request):
        status_, resp_ = auth_user(request)
        if status_:
            try:
                
                user_id = resp_
                snapData = {"snapshot_author":user_id}              
                
                snap_serializer = SnapshotSerializer(data=snapData)
                
                if snap_serializer.is_valid():
                    snap = snap_serializer.save()
                else:
                    print(snap_serializer.errors)
                
                processes = get_process_info()
                
                for proces in processes:
                    proces['snapshot'] = snap.snapshot_id
                    
                serializer = ProcessSerializer(data=processes, many=True)
                
                
                if serializer.is_valid():
                    serializer.save()
                    print("snap git")
                    return Response({"Message":"Snapshot created sucesfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({"ERROR":"Issue with snapshot serializer"},status=status.HTTP_400_BAD_REQUEST)  
                
            except Exception as e:
                return Response({"ERROR":f"{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"ERROR":"Auth error"}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])
def Process_API_kill(request):
        status_, resp_ = auth_user(request)
        if status_:
            try:
                pid = request.POST.get("pid")
                proc_name = request.POST.get("proc_name")
                if pid == None or proc_name == None:
                    return Response({"ERROR":"Must provide PID"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                user_id = resp_

                killLogData = {
                    "KillLog_Author" : user_id,
                    "KillLog_Process_Name" : proc_name,
                    "KillLog_Process_Id" : pid
                    }              

                kill_log_serializer = KillLogSerializer(data=killLogData)

                if kill_log_serializer.is_valid():
                    
                    #try to kill motherfucker here
                    
                    kill_log = kill_log_serializer.save()
                else:
                    print(kill_log_serializer.errors)

                return Response({"Message":f"Killed process with PID: {pid}, Name: {proc_name}"}, status=status.HTTP_200_OK)
            except Exception as e:    
                return Response({"ERROR":f"{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"ERROR":"Auth error"}, status=status.HTTP_401_UNAUTHORIZED)



class Snapshot_browser_view(APIView):   
    def get(self, request):
        status_, resp_ = auth_user(request)
        if status_:
            try:
                
                snap_id = request.GET.get('snap_id')
                
                if snap_id != None:
                        try:
                            snapshot = SnapshotObject.objects.get(snapshot_id=snap_id)
                            processes = ProcessObject.objects.filter(snapshot=snapshot)
                            return render(request, f'{templates_dir}/snap_details.html', {'snapshot': snapshot,'processes':processes})
                        
                        except Exception as e:
                            return render(request, f'{templates_dir}/404.html',{'errors': e})
                            
                else:
                    snapshots = SnapshotObject.objects.all()
                    return render(request, f'{templates_dir}/snapshots.html',{'snapshots': snapshots})
                           
            except Exception as e:
                return Response({"ERROR":f"{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return redirect('/sign-in/') 


    def delete(self, request):
        status_, resp_ = auth_user(request)
        if status_:
            
            snapshot_id = request.data.get('snapshot_id')  
                    
            if snapshot_id == None:
                return Response({"ERROR": "Snapshot ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                snapshot = get_object_or_404(SnapshotObject, snapshot_id=snapshot_id)
                snapshot.delete()
                return Response({"OK": "Snapshot removed"}, status=status.HTTP_200_OK)
            
            except Exception as e:
                return Response({"ERROR": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response({"ERROR":"Auth error"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def Snapshot_API_export(request):
        status_, resp_ = auth_user(request)
        if status_:
            try:
                
                snap_id = request.GET.get('snap_id')
                if snap_id == None:
                    return Response({"ERROR": "Snapshot ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
                
                status_, resp_ = create_excel(snap_id)
                if status_ != True:
                    return Response({"ERROR":f"{resp_}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)       

                return resp_
            except Exception as e:    
                return Response({"ERROR":f"{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"ERROR":"Auth error"}, status=status.HTTP_401_UNAUTHORIZED)




class Kill_Log_browser_view(APIView):    
    def get(self, request):
        status_, resp_ = auth_user(request)
        if status_:
            kills = KillLog_object.objects.all()
            return render(request, f'{templates_dir}/kill-log.html', {'kills': kills})
        else:
            return redirect('/sign-in/') 
        
        
    def delete(self, request):
        status_, resp_ = auth_user(request)
        if status_:
            
            kill_id = request.data.get('kill_id')          
            if kill_id == None:
                return Response({"ERROR": "Kill entry ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                kill_entry = get_object_or_404(KillLog_object, KillLog_ID=kill_id)
                kill_entry.delete()
                return Response({"OK": "Kill entry removed"}, status=status.HTTP_200_OK)
            
            except Exception as e:
                return Response({"ERROR": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response({"ERROR":"Auth error"}, status=status.HTTP_401_UNAUTHORIZED)
    


###########################################################################
#Auth methods


@api_view(['GET'])
def Register_view(request):
    status_, resp_ = auth_user(request)
    if status_:
        return render(request, f'{templates_dir}/index.html')
    else:   
        return render(request, f'{templates_dir}/sign-up.html',{'require_login': True})
    
   


@api_view(['POST'])
def Register_API(request):
    status_, resp_ = auth_user(request)
    if status_:
        return Response({"ERROR":"User logged in"}, status=status.HTTP_403_FORBIDDEN)
    
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
def Login_view(request):
    status_, resp_ = auth_user(request)
    if status_:
        return render(request, f'{templates_dir}/index.html')
    else:   
        return render(request, f'{templates_dir}/sign-in.html',{'require_login': True})



@api_view(['POST'])
def Login_API(request):
    status_, resp_ = auth_user(request)
    if status_:
        return Response({"ERROR":"User already logged in"}, status=status.HTTP_403_FORBIDDEN)
    
    
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    
    if user:
        tokens = get_tokens_for_user(user)  
        response = JsonResponse({"message": "Login successful"})
        response.set_cookie("access_token", tokens["access"], httponly=True, samesite="Strict", secure=True)
        response.set_cookie("refresh_token", tokens["refresh"], httponly=True, samesite="Strict", secure=True)
        response["HX-Redirect"] = "/"
        return response
    else:
        return Response({"ERROR":"Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    



@api_view(['GET'])
def Log_out_API(request):
    status_, resp_ = auth_user(request)
    if status_:
        
        status_2, resp_2 = ban_token(request)
        if status_2:
            response = render(request, f'{templates_dir}/logout.html', {'require_login': True})
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            return response
        else:
            return render(request, f'{templates_dir}/index.html',{'require_login': True})
    else:   
        return render(request, f'{templates_dir}/index.html',{'require_login': True})
        