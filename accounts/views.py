from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserForm
from .models import User


def registerUser(request):

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data["password"]
            user.role = User.CUSTOMER
            user.set_password(password)
            user.save()
            messages.add_message(request, messages.SUCCESS, "Your account has been created successfully")
            return  redirect('registerUser')
    else:
        form = UserForm()

    context = {
        'form':form,
    }
    return render(request, 'accounts/registerUser.html', context)
