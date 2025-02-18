from django.forms import ModelForm
from django import forms
from menu.models import Category
from accounts.validators import allow_only_image_validators
from menu.models import FoodItem

class CategoryForm(ModelForm):
    
    class Meta:
        model = Category
        fields = ["category_name", "description"]


class FoodItemForm(ModelForm):
    
    image = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'btn btn-info w-100'}),
        validators=[allow_only_image_validators]
    )
    class Meta:
        model = FoodItem
        fields = ["category", "food_title", "description", "price", "is_available", "image"]

    def __init__(self, *args, **kwargs):
        vendor = kwargs.pop('vendor', None)  # Get vendor if passed from view
        super(FoodItemForm, self).__init__(*args, **kwargs)
        
        if vendor:
            # Modify queryset to only show categories related to this vendor
            self.fields['category'].queryset = Category.objects.filter(vendor=vendor)