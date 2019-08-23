# coding=utf-8

from django.contrib import admin
from core.models import Book


# Register your models here.
class BookAdmin(admin.ModelAdmin):
    """class docstring"""
    list_display = ('user', 'title', 'author', 'pdf', 'cover')
    fieldsets = (
        (None, {
            'fields': ['user', 'title', 'author', 'pdf', 'cover']
        }
        ),
    )
    filter_horizontal = ()


admin.site.register(Book, BookAdmin)
