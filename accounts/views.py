from django.shortcuts import render
from django.http import HttpResponse


def registerUser(request):
    return render(request, 'accounts/registerUser.html')
