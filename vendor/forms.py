from django.forms import ModelForm
from django import forms
from vendor.models import Vendor, OpeningHour
from accounts.validators import allow_only_image_validators

class VendorForm(ModelForm):
    
    vendor_license = forms.FileField(validators=[allow_only_image_validators])
    class Meta:
        model = Vendor
        fields = ["vendor_name", "vendor_license"]

class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ['day', 'from_hour', 'to_hour', 'is_closed']