from django.forms import ModelForm
from accounts.models import User
from django import forms
from django.core.exceptions import ValidationError
from accounts.models import UserProfile
from accounts.validators import allow_only_image_validators


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

    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Start typing...', 'required': 'required'}))
    profile_picture = forms.FileField(validators=[allow_only_image_validators])
    cover_photo = forms.FileField(validators=[allow_only_image_validators])

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'address', 'country', 'state', 'city', 'pin_code', 'latitude', 'longitude']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            cleaned_data['latitude'] = cleaned_data.get('latitude', instance.latitude)
            cleaned_data['longitude'] = cleaned_data.get('longitude', instance.longitude)
        return cleaned_data


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']