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