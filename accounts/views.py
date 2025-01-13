from django.shortcuts import render
from django.http import HttpResponse


def registerUser(request):
    return HttpResponse("This is user registeration form")
