from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserForm
from accounts.models import UserProfile
from vendor.forms import VendorForm
from .models import User
from django.contrib.auth import authenticate, login, logout
from accounts.utils import detectUser
from django.contrib.auth.decorators import login_required


def registerUser(request):

    if request.user.is_authenticated:
        messages.add_message(request, messages.WARNING, 'You are already logged in')
        return redirect(my_account)

    elif request.method == 'POST':
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

    if request.user.is_authenticated:
        messages.add_message(request, messages.WARNING, 'You are already logged in')
        return redirect(my_account)

    elif request.method == 'POST':
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


def user_login(request):

    if request.user.is_authenticated:
        messages.add_message(request, messages.WARNING, 'You are already logged in')
        return redirect(my_account)

    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'You are logged in')
            redirectUrl = detectUser(user)
            return redirect(my_account)
        else:
            messages.add_message(request, messages.ERROR, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')


def user_logout(request):

    logout(request)
    messages.add_message(request, messages.INFO, 'You are logged out')
    return redirect('login')


@login_required(login_url='login')
def my_account(request):

    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


@login_required(login_url='login')
def vendorDashboard(request):

    return render(request, 'accounts/vendorDashboard.html')


@login_required(login_url='login')
def customerDashboard(request):

    return render(request, 'accounts/customerDashboard.html')