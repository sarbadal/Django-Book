# coding=utf-8

from django import forms
from core.models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'pdf', 'cover')
