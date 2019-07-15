# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Book, Employee, Book_Author, User_Data

# Register your models here.

admin.site.register(Book)
admin.site.register(Employee)
admin.site.register(Book_Author)
admin.site.register(User_Data)

admin.site.site_header = 'Book Store'
admin.site.index_title = 'Online Book Storage App'
