# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.contrib.auth import login, authenticate
# from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, BookForm, BookAuthorForm, UpdateBookForm, EmployeeForm, UpdateEmployeeForm, \
    UserDataForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login, authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from .models import Book, Book_Author, Employee, User_Data
from django import template
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json


# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            fs= form.save(commit=False)
            fs.current_user= request.user.id
            fs.save()
            # form.save()
            messages.add_message(request, messages.INFO,
                                 'You have been successfully registered, now you can Login.')
            return redirect('user_login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect(home)
        else:
            messages.add_message(request, messages.INFO, 'The username and/or password you specified are not correct.')
            return redirect('user_login')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect(user_login)


register = template.Library()


@login_required
def home(request):
    return render(request, 'home.html', {})


@login_required
def add_book_author(request):
    if request.method == 'POST':
        form = BookAuthorForm(request.POST)
        if form.is_valid():
            fs= form.save(commit=False)
            fs.current_user= request.user.id
            fs.save()

            # form.save()
            messages.add_message(request, messages.SUCCESS, 'Added Book Author Successfully...!')
            return redirect(add_book_author)
    else:
        form = BookAuthorForm()
    return render(request, 'add_book_author.html', {'form': form})


@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.current_user = request.user.id
            fs.save()
            # form.save()
            messages.add_message(request, messages.INFO, 'Saved Successfully...!')
            return redirect(add_book)
        else:
            if request.method == 'POST':
                form = BookForm()
                book_obj = Book.objects.filter(current_user=request.user.id)
                page = request.GET.get('page', 1)
                paginator = Paginator(book_obj, 3)
                user = paginator.page(page)

                book_title = request.POST.get('book_title')
                series = request.POST.get('series')
                author_name = request.POST.get('author_name')
                pages = request.POST.get('pages')

                if book_title and series:
                    search_book_obj = Book.objects.filter(book_title__icontains=book_title, series=series,
                                                          current_user=request.user.id)
                    return render(request, 'add_book.html',
                                  {'form': form, 'books': user, 'search_book': search_book_obj})

                elif series:
                    search_book_obj = Book.objects.filter(series__icontains=series, current_user=request.user.id)
                    return render(request, 'add_book.html',
                                  {'form': form, 'books': user, 'search_book': search_book_obj})

                elif author_name:
                    search_book_obj1 = Book_Author.objects.filter(name__icontains=author_name,
                                                                  current_user=request.user.id)
                    if search_book_obj1:
                        search_book_obj = Book.objects.filter(author_name=search_book_obj1,
                                                              current_user=request.user.id)
                        return render(request, 'add_book.html',
                                      {'form': form, 'books': user, 'search_book': search_book_obj})
                    else:
                        return render(request, 'add_book.html', {'form': form, 'books': user})

                elif pages:
                    search_book_obj = Book.objects.filter(pages__icontains=pages, current_user=request.user.id)
                    return render(request, 'add_book.html',
                                  {'form': form, 'books': user, 'search_book': search_book_obj})

                elif book_title:
                    search_book_obj = Book.objects.filter(book_title__icontains=book_title,
                                                          current_user=request.user.id)
                    return render(request, 'add_book.html',
                                  {'form': form, 'books': user, 'search_book': search_book_obj})
                else:
                    return render(request, 'add_book.html', {'form': form, 'books': user})
            else:
                return redirect('add_book')
    else:
        form = BookForm()

        book_obj = Book.objects.filter(current_user=request.user.id)

        page = request.GET.get('page', 1)
        paginator = Paginator(book_obj, 3)
        try:
            user = paginator.page(page)
        except PageNotAnInteger:
            user = paginator.page(1)
        except EmptyPage:
            user = paginator.page(paginator.num_pages)
        return render(request, 'add_book.html', {'form': form, 'books': user})
