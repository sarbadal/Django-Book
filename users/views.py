# coding=utf-8

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from accounts.models import CustomUser
from core.models import Book
from core.forms import BookForm
from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from users.token import activation_token


@login_required
def user_home(request):
    """Users Home"""
    books = Book.objects.filter(user=request.user)
    return render(
        request,
        'users/book_list_user.html',
        {'books': books}
    )


def register(request, *args, **kwargs):
    """User registration view"""

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_active = False
            instance.save()

            site = get_current_site(request)
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            email = form.cleaned_data.get('email')
            message_html = render_to_string(
                'users/verify_email.html',
                {
                    'user': instance,
                    'username': username,
                    'first_name': first_name,
                    'email': email,
                    'domain': site.domain,
                    'uid': instance.id,
                    'token': activation_token.make_token(instance)
                }
            )
            send_mail(
                'Confirmation message - watchthecityweather.com',
                message_html,
                'watchthecityweather@gmail.com',
                [email],
                fail_silently=True
            )

            return render(request, 'users/registration_start.html')
    else:
        form = UserRegisterForm()

    return render(
        request,
        'users/register.html',
        {
            'form': form,
            'title': 'Registration'
        }
    )


@login_required
def profile(request):
    """Docstring"""

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST,
            instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('home')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': 'Profile',
    }

    return render(request, 'users/profile.html', context)


@login_required
def change_password(request):
    """Docstring"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request,
                'Your password was successfully updated!'
            )

            return redirect('home')

        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(
        request,
        'users/change_password.html',
        {'form': form, 'title': 'Change Password'}
    )


def activate_user_account(request, uid, token):
    """activate user account through email"""
    user = get_object_or_404(CustomUser, pk=uid)

    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        return render(request, 'users/registration_complete.html')

    else:
        return render(request, 'users/registration_error.html')


def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('home')
    else:
        form = BookForm()

    return render(request, 'book/upload.html', {'form': form})


def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')
