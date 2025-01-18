from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User


def registerUser(request):

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user = form.save(commit=False)
            password = form.cleaned_data["password"]
            user.role = User.CUSTOMER
            user.set_password(password)
            user.save()
            return  redirect('registerUser')

        else:
            print(f"field.errors {form.errors}")
            print(f"non_field error {form.non_field_errors}")
            # first_name = form.cleaned_data["first_name"]
            # last_name = form.cleaned_data["last_name"]
            # username = form.cleaned_data["username"]
            # email = form.cleaned_data["email"]
            # password = form.cleaned_data["password"]
            # user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            # user.role = User.CUSTOMER
            # user.save()
            # return  redirect('registerUser')
    else:
        form = UserForm()

    context = {
        'form':form,
    }
    return render(request, 'accounts/registerUser.html', context)
