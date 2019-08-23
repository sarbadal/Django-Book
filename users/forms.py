# coding=utf-8

from django import forms
from phonenumber_field.modelfields import PhoneNumberField
from accounts.models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from users.models import Profile


class UserRegisterForm(UserCreationForm):
    """class docstring"""
    email = forms.EmailField()
    first_name = forms.CharField(label='First Name', required=True)
    last_name = forms.CharField(label='Last Name', required=False)

    class Meta:
        """Meta class"""
        model = CustomUser
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2'
        ]


class UserUpdateForm(forms.ModelForm):
    """class docstring"""
    first_name = forms.CharField(label='First Name', required=True)
    last_name = forms.CharField(label='Last Name', required=False)

    class Meta:
        """Meta class"""
        model = CustomUser
        fields = ['first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    """class docstring"""
    phone_number = PhoneNumberField()

    class Meta:
        """Meta class"""
        model = Profile
        fields = ['phone_number']
