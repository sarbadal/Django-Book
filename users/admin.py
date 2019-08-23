# coding=utf-8

from django.contrib import admin
from users.models import Profile

# Register your models here.
admin.site.site_header = 'Book Admin Page'


class ProfileAdmin(admin.ModelAdmin):
    """class docstring"""
    list_display = ['user', 'phone_number']


admin.site.register(Profile, ProfileAdmin)
