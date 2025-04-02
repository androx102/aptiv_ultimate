from django.urls import path
from .views import (
    index,
    ProcessBrowserView,
    ProcessBrowserSnapAPI,
    ProcessBrowserKillAPI,
    SnapshotBrowserView,
    SnapshotExportAPI,
    KillLogBrowserView,
    LogOutAPI,
    LoginAPI,
    RegisterAPI,
    RegisterView,
    LoginView,
)


urlpatterns = [
    # Index page
    path("", index.as_view(), name="index"),
    #
    ########## Process browser ##########
    # 1. Display page and processes data table -> return htmx
    path("processes/", ProcessBrowserView.as_view(), name="processes"),
    # Tested: 3/3
    # 2. Take snapshot -> return json
    path("API/processes/snap/", ProcessBrowserSnapAPI.as_view(), name="take_snapshot"),
    # Tested: 2/3
    # TODO:
    # - fix test_take_snapshot_fail
    # Kill process -> return json
    path("API/processes/kill/", ProcessBrowserKillAPI.as_view(), name="kill_proc"),
    # Tested: 3/3
    ########## Snapshot browser ##########
    # 1. Display page -> return htmx
    path("snapshots/", SnapshotBrowserView.as_view(), name="snapshots"),
    # Tested: 6/6
    # 2. Export to excel -> return file
    path("API/snap/excel/", SnapshotExportAPI.as_view(), name="export_snap"),
    # Tested: 2/3
    # TODO:
    # - fix test_export_snapshot_fail
    ########## Kill log interface ##########
    # 1. Display page -> return htmx
    path("kill-log/", KillLogBrowserView.as_view(), name="kill-log"),
    # Tested: 3/3
    ########## Auth ##########
    # 1. Sign-in page -> return htmx
    path("sign-in/", LoginView.as_view(), name="sign_in"),
    # Tested: 2/2
    # 2. Sign-in endpoint -> retunr json
    path("API/sign-in/", LoginAPI.as_view(), name="sign_in_api"),
    # Tested: 3/3
    # 3. Sign-up page -> -> return htmx
    path("sign-up/", RegisterView.as_view(), name="sign_up"),
    # Tested: 2/2
    # 4. Sign-up endpoint -> retunr json
    path("API/sign-up/", RegisterAPI.as_view(), name="sign_up_api"),
    # Tested: 4/4
    # 5. Logout
    path("API/log-out/", LogOutAPI.as_view(), name="logout"),
    # Tested: 0/2
    # TODO:
    # - add test_logout_sucess
    # - add test_logout_invalid_token_fail
]
