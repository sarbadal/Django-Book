# coding=utf-8

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from core.models import Book


# Create your views here.
def home(request):
    """Render Home Page"""
    books = Book.objects.all()
    return render(request, 'book/book_list.html', {'books': books})


def upload_book_old(request):
    """Book Upload view"""
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'book/upload.html', context)
