from django.urls import path, re_path, include
from .views import *



urlpatterns = [
    
    #Process browser
    # 1. Display page -> return htmx
    path('proc-browser/', Process_browser_view.as_view(), name="Process browser view"),
    
    # 2. Get list of processes -> return json
    path('API/processes/', Process_API, name="Return list of processes"),
    
    # 3. Take snapshot -> return json
    #path('API/processes/<str:id>', Process_API, name="Takes snapshot"),
    
    # 4. Kill process -> return json
    #path('API/processes/<str:id>', Process_API, name="Takes snapshot"),
    
    
    
    
    #Snapshot browser
    # 1. Display page -> return htmx
    path('snap-browser/', Snapshot_browser_view.as_view(), name="Snapshot browser view"),
    
    # 2. Get list of snapshots -> return json
    
    # 3. Export to excel -> return file (file storage for bigger files?)
    
    
    #Kill log interface
    # 1. Display page -> return htmx
    path('kill-browser/', Kill_Log_browser_view.as_view(), name="Kill log browser view"),
    
    # 2. Get list of killed processes -> return json
    
    
    #Auth
    # 1. Sign-in page -> return htmx
    path('sign-in/', Login_view.as_view(), name="Sign-IN view"),
    
    # 2. Sign-in endpoint -> retunr json
    
    # 3. Sign-up page -> -> return htmx
    path('sign-up/', Register_view.as_view(), name="Sign-UP view"),
    
    # 3. Sign-up endpoint -> retunr json
]