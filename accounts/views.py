# coding=utf-8

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from accounts.forms import UserLoginForm


# Create your views here.

def login_view(request, *args, **kwargs):
    """Docstring"""
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        user_obj = form.cleaned_data.get('user_obj')
        login(request, user_obj)
        return redirect('home')

    return render(
        request,
        'users/login.html',
        {"form": form, 'title': 'Login'}
    )


def logout_view(request):
    """Docstring"""
    logout(request)
    return redirect("login")
