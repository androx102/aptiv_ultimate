from django.urls import path, re_path, include
from .views import *



urlpatterns = [
    
    #Process browser
    # 1. Display page -> return htmx
    path('proc_browser', Process_browser_view.as_view(), name="Process browser view"),
    
    # 2. Get list of processes -> return json
    path('proc_browser/processes/', Process_API, name="Return list of processes"),
    
    

    # 3. Take snapshot -> return json
    #path('API/processes/<str:id>', Process_API, name="Takes snapshot"),
    
    # 4. Kill process -> return json
    #path('API/processes/<str:id>', Process_API, name="Takes snapshot"),
    
    
    
    
    #Snapshot browser
    # 1. Display page -> return htmx
    # 2. Get list of snapshots -> return json
    # 3. Export to excel -> return file (file storage for bigger files?)
    
    
    #Kill log interface
    # 1. Display page -> return htmx
    # 2. Get list of killed processes -> return json
    
    
    #Auth
    # 1. Sign-in page -> return htmx
    # 2. Sign-in endpoint -> retunr json
    # 3. Sign-up page -> -> return htmx
    # 3. Sign-up endpoint -> retunr json
]