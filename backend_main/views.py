from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, generics
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
import pathlib

templates_dir = pathlib.Path(__file__).resolve().parent / "templates"






class Process_browser_view(View):
    def get(self, request):
        return render(request, f'{templates_dir}/process_browser.html')



@api_view(['GET'])
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
    

   


