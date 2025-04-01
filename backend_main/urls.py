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
    #
    ########## Process browser ##########
    # 1. Display page and processes data table -> return htmx
    path("processes/", Process_browser_view.as_view(), name="processes"),
    # Tested: 3/3  
    # 2. Take snapshot -> return json
    path("API/processes/snap/", Process_API_snap.as_view(), name="take_snapshot"),
    # Tested: 1/3
    # TODO:
    # - add test for take_snapshot_sucess
    # - add test for take_snapshot_fail
    # Kill process -> return json
    path("API/processes/kill/", Process_API_kill.as_view(), name="kill_proc"),
    # Tested: 1/3
    # TODO:
    # - add test for kill_process_sucess
    # - add test for kill_process_fail
    ########## Snapshot browser ##########
    # 1. Display page -> return htmx
    path("snapshots/", Snapshot_browser_view.as_view(), name="snapshots"),
    # Tested: 6/6
    # 2. Export to excel -> return file
    path("API/snap/excel/", Snapshot_API_export.as_view(), name="export_snap"),
    # Tested: 3/3
    ########## Kill log interface ##########
    # 1. Display page -> return htmx
    path("kill-log/", Kill_Log_browser_view.as_view(), name="kill-log"),
    # Tested: 4/4
    ########## Auth ##########
    # 1. Sign-in page -> return htmx
    path("sign-in/", Login_view.as_view(), name="sign_in"),
    # Tested: 2/2
    # 2. Sign-in endpoint -> retunr json
    path("API/sign-in/", Login_API.as_view(), name="sign_in_api"),
    # Tested: 3/3
    # 3. Sign-up page -> -> return htmx
    path("sign-up/", Register_view.as_view(), name="sign_up"),
    # Tested: 2/2
    # 4. Sign-up endpoint -> retunr json
    path("API/sign-up/", Register_API.as_view(), name="sign_up_api"),
    # Tested: 4/4
    # 5. Logout
    path("API/log-out/", Log_out_API.as_view(), name="logout"),
    # Tested: 0/2
    # TODO:
    # - add test_logout_sucess
    # - add test_logout_invalid_token_fail
]
