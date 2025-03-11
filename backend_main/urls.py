from django.urls import path, re_path, include
from .views import home_view



urlpatterns = [
    #Process browser
    # 1. Display page -> return htmx
    path('test/', home_view, name="Process browser view"),#processbrowser
    # 2. Get list of processes -> return json
    # 3. Take snapshot -> return json
    # 4. Kill process -> return json
    
    
    
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