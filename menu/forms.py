from django.forms import ModelForm
from django import forms
from menu.models import Category
from accounts.validators import allow_only_image_validators

class CategoryForm(ModelForm):
    
    class Meta:
        model = Category
        fields = ["category_name", "description"]


class FoodItemForm(ModelForm):
    
    image = forms.FileField(validators=[allow_only_image_validators])
    class Meta:
        model = FoodItem
        fields = ["category", "food_title", "description", "price", "is_available", "image"]