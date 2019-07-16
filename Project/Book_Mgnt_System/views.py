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
            fs = form.save(commit=False)
            fs.current_user = request.user.id
            fs.save()
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


# register = template.Library()


@login_required
def home(request):
    return render(request, 'home.html', {})


@login_required
def add_book_author(request):
    if request.method == 'POST':
        form = BookAuthorForm(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.current_user = request.user.id
            fs.save()

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


@login_required
def delete_book(request, id):
    book_obj = Book.objects.get(id=id)
    book_obj.delete()
    messages.add_message(request, messages.INFO, 'Delete Successfully...!')
    return redirect('add_book')


@login_required
def update_book(request, id):
    book_obj = Book.objects.get(id=id)
    if request.method == 'POST':
        form = UpdateBookForm(request.POST, instance=book_obj)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.current_user = request.user.id
            fs.save()
            messages.add_message(request, messages.INFO, 'Update Successfully...!')
            return redirect('add_book')
        return render(request, 'update_book.html', {'form': form})
    else:
        form = UpdateBookForm(instance=book_obj)
    return render(request, 'update_book.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.current_user = request.user.id
            fs.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, _('Your password was successfully updated!'))
            return redirect('change_password')
        else:
            messages.error(request, _('Please correct the error.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


@login_required
def group(request):
    group_obj = Group.objects.filter(current_user=request.user.id)
    group_obj2 = Group.objects.get(name='All_User')
    group_obj3 = Group.objects.filter(name='Test')
    group = Group.objects.get(name='MyGroup')
    user = User.objects.get(username='gaurav')
    user.groups.add(group)
    return HttpResponse("Group test...!")


@login_required
def add_employee(request):
    emp_obj = None
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.current_user = request.user.id
            fs.save()
            # form.save()
            messages.add_message(request, messages.INFO, 'Added successfully...!')
            return redirect('add_employee')
    else:
        form = EmployeeForm()
        emp_obj = Employee.objects.filter(current_user=request.user.id)
    return render(request, 'add_employee.html', {'form': form, 'employee': emp_obj})


@login_required
def delete_employee(request, id):
    emp_obj = Employee.objects.get(id=id)
    emp_obj.delete()
    messages.add_message(request, messages.INFO, 'Delete Successfully...!')
    return redirect('add_employee')


@login_required
def edit_employee(request, id):
    emp_obj = Employee.objects.get(id=id)
    if request.method == 'POST':
        form = UpdateEmployeeForm(request.POST, instance=emp_obj)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.current_user = request.user.id
            fs.save()
            messages.add_message(request, messages.INFO, 'Update Successfully...!')
            return redirect('add_employee')
        return render(request, 'update_employee.html', {'form': form})
    else:
        form = UpdateEmployeeForm(instance=emp_obj)
    return render(request, 'update_employee.html', {'form': form})


@login_required
def user_data(request):
    if request.method == 'POST':
        form = UserDataForm(request.POST)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.current_user = request.user.id
            fs.save()

            username = request.POST.get('username')
            age = request.POST.get('age')

            messages.add_message(request, messages.INFO, 'Added successfully...!')
            return redirect('userdata')
    else:
        form = UserDataForm()
    return render(request, 'userdata.html', {'form': form})


@login_required
def get_book_data(request):
    data = json.loads(request.POST.get("data"))
    print(data)
    if data:
        book_title = None
        author_name = None
        book_image = None
        book_id = None
        series = None
        description = None
        pages = None
        for item in data:
            book_title = item.get('ajax_book_title', None)

            image = item.get('ajax_book_image', None)
            book_image1 = image.split('/', 2)[2]
            book_image = "/" + book_image1

            book_id = item.get('ajax_id', None)
            author_name = item.get('ajax_author_name', None)
            series = item.get('ajax_series', None)
            description = item.get('ajax_description', None)
            pages = item.get('ajax_pages', None)

        if book_title:
            book_author_obj = Book_Author.objects.get(name=author_name)
            book_obj = Book(book_title=book_title, book_image=book_image, id=book_id, series=series,
                            description=description, pages=pages, author_name=book_author_obj,
                            current_user=request.user.id)
            book_obj.save()
            return JsonResponse(True, safe=False)

    else:
        return JsonResponse(False, safe=False)


# @login_required
# def get_book_data(request):
# 	if request.method == 'POST':
# 		if request.is_ajax():
# 			book_title  = request.POST.get('ajax_book_title')
# 			book_image  = request.FILES.get('ajax_book_image')
# 			book_id 	= request.POST.get('ajax_id')
# 			author_name = request.POST.get('ajax_author_name')
# 			series 	 	= request.POST.get('ajax_series')
# 			description = request.POST.get('ajax_description')
# 			pages 		= request.POST.get('ajax_pages')
#
# 			if book_title:
# 				book_author_obj = Book_Author.objects.get(name=author_name)
# 				book_obj = Book(book_title=book_title, book_image=book_image, id=book_id, series=series,
# 								description=description, pages=pages, author_name=book_author_obj)
# 				book_obj.save()
# 				return JsonResponse(True, safe=False)
# 			else:
# 				return JsonResponse(False, safe=False)
# 		else:
# 			print "Ajax not working"
# 	else:
# 			print "Ajax not working"


@login_required
def delete_book_data(request):
    if request.method == 'POST':
        if request.is_ajax():
            book_id = request.POST.get('id')
            if book_id:
                book_obj = Book.objects.get(id=book_id)
                book_obj.delete()
                return JsonResponse(True, safe=False)
        else:
            JsonResponse(False, safe=False)
