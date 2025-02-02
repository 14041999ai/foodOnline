from django.forms import ModelForm
from accounts.models import User
from django import forms
from django.core.exceptions import ValidationError
from accounts.models import UserProfile


class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_manager', 'role']

    def clean(self):

        cleaned_data = super().clean()
        password = cleaned_data["password"]
        confirm_password = cleaned_data["confirm_password"]
        if  password != confirm_password:
            raise forms.ValidationError(
                    "Password does not match!"
                )


class UserProfileForm(ModelForm):

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'pin_code', 'latitude', 'longitude']
