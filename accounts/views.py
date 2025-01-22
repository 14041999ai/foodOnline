from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserForm
from accounts.models import UserProfile
from vendor.forms import VendorForm
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


def registerVendor(request):

    if request.method == 'POST':

        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data["password"]
            user.role = User.VENDOR
            user.set_password(password)
            user.save()

            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor.user_profile = UserProfile.objects.get(user=user)
            vendor.save()
            messages.add_message(request, messages.SUCCESS, "Your account has been created successfully. Please wait for approval.")
            return redirect('registerVendor')
    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form
    }

    return render(request, 'accounts/registerVendor.html', context)

def login(request):
    return render(request, 'accounts/login.html')


def logout(request):
    pass


def dashboard(request):
    pass