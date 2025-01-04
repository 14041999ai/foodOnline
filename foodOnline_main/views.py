from django.shortcuts import render
from django.http import HttpResponse

def home(reqquest):
    return HttpResponse("Hello World")