from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserForm
from accounts.models import UserProfile
from vendor.forms import VendorForm
from .models import User
from django.contrib.auth import authenticate, login, logout
from accounts.utils import detectUser, send_verification_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator


def check_role_vendor(user):

    if user.role == 1:
        return True
    else:
        raise PermissionDenied


def check_role_customer(user):

    if user.role == 2:
        return True
    else:
        raise PermissionDenied


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

            # send verification email
            mail_subject = 'Activation link has been sent to your email address'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)

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

            # send verification email
            mail_subject = 'Activation link has been sent to your email address'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)

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


def activate(request, uidb64, token):
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Congratulations Your account is activated. ')
        return redirect('my_account')
    else:
        messages.add_message(request, messages.ERROR, 'Invalid activation link')
        return redirect('my_account')



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
@user_passes_test(check_role_vendor)
def vendorDashboard(request):

    return render(request, 'accounts/vendorDashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customerDashboard(request):

    return render(request, 'accounts/customerDashboard.html')


def forgot_password(request):

    if request.method == 'POST':
        #check if user with email exist .If true then send the reset password link else return error
        email = request.POST['email']
        user = User.objects.get(email__exact=email)
        if user is not None:
            mail_subject = 'Reset your password'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.add_message(request, messages.SUCCESS, 'Password reset link is sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')


def reset_password_validate (request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.add_message(request, messages.INFO, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.add_message(request, messages.ERROR, 'This link has been expired!')
        return redirect('my_account')
        
    return render(request, 'accounts/forgot_password.html')


def reset_password(request):

    if request.method == 'POST':
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Password reset successfully')
            return redirect('login')
            pass
        else:
            messages.add_message(request, messages.ERROR, 'Password do not match!')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')
