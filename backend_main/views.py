from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import redirect
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
import pathlib
from .models import ProcessObject, SnapshotObject, KillLog_object
from .auth_utils import ban_token, get_tokens_for_user
from .serializers import (
    UserSerializer,
    ProcessSerializer,
    SnapshotSerializer,
    KillLogSerializer,
)
from .utils import get_process_info, kill_proc_by_id, create_excel


templates_dir = pathlib.Path(__file__).resolve().parent / "templates" / "backend_main"
partials_dir = pathlib.Path(__file__).resolve().parent / "templates" / "partials"


class index(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        auth_required = not request.user.is_authenticated
        return render(
            request, f"{templates_dir}/index.html", {"auth_required": auth_required}
        )


class Process_browser_view(APIView):
    def get(self, request):
        processes = get_process_info()
        if request.headers.get("HX-Request") == "true":
            return render(
                request,
                f"{partials_dir}/proc_table.html",
                {"processes": processes},
            )
        else:
            return render(
                request,
                f"{templates_dir}/proc-browser.html",
                {"processes": processes},
            )


class Process_API_snap(APIView):
    def get(self, request):
        user_id = request.user.id
        snapData = {"snapshot_author": user_id}
        snap_serializer = SnapshotSerializer(data=snapData)

        if snap_serializer.is_valid():
            snap = snap_serializer.save()
        else:
            return Response(snap_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        processes = get_process_info()

        for proces in processes:
            proces["snapshot"] = snap.snapshot_id

        proc_serializer = ProcessSerializer(data=processes, many=True)

        if proc_serializer.is_valid():
            proc_serializer.save()
            return Response(
                {"Message": "Snapshot created sucesfully"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(proc_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Process_API_kill(APIView):
    def post(self, request):
        user_id = request.user.id
        pid = request.POST.get("pid")
        proc_name = request.POST.get("proc_name")

        if pid == None or proc_name == None:
            return Response(
                {"ERROR": "Must provide PID"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        killLogData = {
            "KillLog_Author": user_id,
            "KillLog_Process_Name": proc_name,
            "KillLog_Process_Id": pid,
        }

        kill_log_serializer = KillLogSerializer(data=killLogData)

        if kill_log_serializer.is_valid():
            status_, message_ = kill_proc_by_id(int(pid))
            kill_log = kill_log_serializer.save()
        else:
            return Response(
                kill_log_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        processes = get_process_info()
        if request.headers.get("HX-Request") == "true":
            return render(
                request,
                f"{partials_dir}/proc_table.html",
                {"processes": processes},
            )


class Snapshot_browser_view(APIView):
    def get(self, request):
        snap_id = request.GET.get("snap_id")

        if snap_id != None:
            snapshot = get_object_or_404(SnapshotObject, snapshot_id=snap_id)
            processes = get_list_or_404(ProcessObject, snapshot=snapshot)
            return render(
                request,
                f"{templates_dir}/snap_details.html",
                {"snapshot": snapshot, "processes": processes},
            )
        else:
            snapshots = SnapshotObject.objects.all()
            return render(
                request,
                f"{templates_dir}/snapshots.html",
                {"snapshots": snapshots},
            )

    def delete(self, request):
        snapshot_id = request.data.get("snapshot_id")

        if snapshot_id == None:
            return Response(
                {"ERROR": "Snapshot ID not provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        snapshot = get_object_or_404(SnapshotObject, snapshot_id=snapshot_id)
        snapshot.delete()

        snapshots = SnapshotObject.objects.all()
        return render(
            request,
            f"{partials_dir}/snap_table.html",
            {"snapshots": snapshots},
        )


class Snapshot_API_export(APIView):
    def get(self, request):
        snap_id = request.GET.get("snap_id")
        if snap_id == None:
            return Response(
                {"ERROR": "Snapshot ID not provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        status_, resp_ = create_excel(snap_id)
        if status_ != True:
            return Response(
                {"ERROR": f"{resp_}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return resp_


class Kill_Log_browser_view(APIView):
    def get(self, request):
        kills = KillLog_object.objects.all()
        return render(request, f"{templates_dir}/kill-log.html", {"kills": kills})

    def delete(self, request):
        kill_id = request.data.get("kill_id")
        if kill_id == None:
            return Response(
                {"ERROR": "Kill entry ID not provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        kill_entry = get_object_or_404(KillLog_object, KillLog_ID=kill_id)
        kill_entry.delete()
        return Response({"OK": "Kill entry removed"}, status=status.HTTP_200_OK)


###########################################################################
# Auth methods


class Register_view(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        else:
            return render(
                request, f"{templates_dir}/sign-up.html", {"auth_required": True}
            )


class Register_API(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("/")

        usr_serializer = UserSerializer(data=request.data)

        if usr_serializer.is_valid():
            usr_serializer.save()
            return Response(
                {"OK": "User created sucesfully"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(usr_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login_view(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        else:
            return render(
                request, f"{templates_dir}/sign-in.html", {"auth_required": True}
            )


class Login_API(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("/")

        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            tokens = get_tokens_for_user(user)
            response = JsonResponse({"message": "Login successful"})
            response.set_cookie(
                "access_token",
                tokens["access"],
                httponly=True,
                samesite="Strict",
                secure=True,
            )

            response.set_cookie(
                "refresh_token",
                tokens["refresh"],
                httponly=True,
                samesite="Strict",
                secure=True,
            )
            response["HX-Redirect"] = "/"
            return response
        else:
            return Response(
                {"ERROR": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class Log_out_API(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("/")

        status_, resp_ = ban_token(request)
        if status_:
            response = render(
                request, f"{templates_dir}/logout.html", {"require_login": True}
            )
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            return response
        else:
            return redirect("/")
