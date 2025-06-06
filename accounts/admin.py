from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin 
from django.contrib.sessions.models import Session
from django.contrib.gis.admin import GISModelAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'role', 'is_active')
    ordering = ('-date_joined', )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(UserProfile, GISModelAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Session)