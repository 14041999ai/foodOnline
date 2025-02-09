from django.urls import path
from . import views
from accounts import views as  Accountviews

urlpatterns = [
    path('', Accountviews.vendorDashboard),
    path('profile/', views.vprofile, name='vprofile'),
    path('menu-builder/', views.menu_builder, name="menu_builder"),
]

