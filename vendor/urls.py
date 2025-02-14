from django.urls import path
from . import views
from accounts import views as  Accountviews

urlpatterns = [
    path('', Accountviews.vendorDashboard),
    path('profile/', views.vprofile, name='vprofile'),
    path('menu-builder/', views.menu_builder, name="menu_builder"),
    path('menu-builder/category/<int:pk>', views.food_items_by_category, name='food_items_by_category'),
    path('menu-builder/category/add', views.add_category, name='add_category'),
    path('menu-builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('menu-builder/food/add', views.add_food, name='add_food'),
]

