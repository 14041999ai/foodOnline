from django.urls import path
from . import views
from accounts import views as  Accountviews

urlpatterns = [
    path('', Accountviews.vendorDashboard),
    path('profile/', views.vprofile, name='vprofile'),
    path('menu-builder/', views.menu_builder, name="menu_builder"),
    # category CRUD operations

    path('menu-builder/category/<int:pk>', views.food_items_by_category, name='food_items_by_category'),
    path('menu-builder/category/add', views.add_category, name='add_category'),
    path('menu-builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('menu-builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),

    # foodItem CRUD operations
    path('menu-builder/food/add', views.add_food, name='add_food'),
    path('menu-builder/food/edit/<int:pk>/', views.edit_food, name='edit_food'),
    path('menu-builder/food/delete/<int:pk>/', views.delete_food, name='delete_food'),

    # opening hour crud
    path('opening-hours/', views.opening_hours, name='opening_hours'),
    path('opening-hours/add/', views.add_opening_hours, name='add_opening_hours'),
    path('opening-hours/remove/<int:pk>', views.remove_opening_hours, name='remove_opening_hours'),
]

