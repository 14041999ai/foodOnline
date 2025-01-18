from django.shortcuts import render,redirect
from django.http import HttpResponse
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
            return  redirect('registerUser')

        else:
            print(f"non_field error {form.non_field_errors}")
    else:
        form = UserForm()

    context = {
        'form':form,
    }
    return render(request, 'accounts/registerUser.html', context)
