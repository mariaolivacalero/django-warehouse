from django.shortcuts import render
from django.http import HttpResponse

def management(request):
    return HttpResponse("Hello world!")