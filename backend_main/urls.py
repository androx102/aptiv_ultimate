from django.urls import path
from .views import (
    index,
    Process_browser_view,
    Process_API_snap,
    Process_API_kill,
    Snapshot_browser_view,
    Snapshot_API_export,
    Kill_Log_browser_view,
    Log_out_API,
    Login_API,
    Register_API,
    Register_view,
    Login_view,
)


urlpatterns = [
    # Index page
    path("", index.as_view(), name="index"),
    # Process browser
    # 1. Display page and processes data table -> return htmx
    path("processes/", Process_browser_view.as_view(), name="processes"),
    # 2. Take snapshot -> return json
    path("API/processes/snap/", Process_API_snap.as_view(), name="take_snapshot"),
    # 3. Kill process -> return json
    path("API/processes/kill/", Process_API_kill.as_view(), name="kill_proc"),
    # Snapshot browser
    # 1. Display page -> return htmx
    path("snapshots/", Snapshot_browser_view.as_view(), name="snapshots"),
    # 2. Export to excel -> return file
    path("API/snap/excel/", Snapshot_API_export.as_view(), name="export_snap"),
    # Kill log interface
    # 1. Display page -> return htmx
    path("kill-log/", Kill_Log_browser_view.as_view(), name="kill-log"),
    # Auth
    # 1. Sign-in page -> return htmx
    path("sign-in/", Login_view.as_view(), name="sign_in"),
    # 2. Sign-in endpoint -> retunr json
    path("API/sign-in/", Login_API.as_view(), name="sign_in_api"),
    # 3. Refresh token endpoint -> return json //Even needed ?!?
    # 4. Sign-up page -> -> return htmx
    path("sign-up/", Register_view.as_view(), name="sign_up"),
    # 5. Sign-up endpoint -> retunr json
    path("API/sign-up/", Register_API.as_view(), name="sign_up_api"),
    # 6. Logout
    path("API/log-out/", Log_out_API.as_view(), name="logout"),
]
