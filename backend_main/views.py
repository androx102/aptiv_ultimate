from django.shortcuts import render
from django.http import HttpResponse
import pathlib



def home_view(request):
    
    return HttpResponse("<h1>Ahoj</h1>")


