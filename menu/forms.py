from django.forms import ModelForm
from django import forms
from menu.models import Category

class CategoryForm(ModelForm):
    
    class Meta:
        model = Category
        fields = ["category_name", "description"]