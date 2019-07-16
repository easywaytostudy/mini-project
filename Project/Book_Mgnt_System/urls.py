"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('accounts/login/', views.user_login, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('home', views.home, name='home'),
    path('add_book', views.add_book, name='add_book'),

    path('add-book-author', views.add_book_author, name='add_book_author'),
    path('delete_book/<int:id>/', views.delete_book, name='delete_book'),
    path('edit_book/<int:id>/', views.update_book, name='edit_book'),
    path('change_password', views.change_password, name='change_password'),
    path('group', views.group, name='group'),
    path('add_employee', views.add_employee, name='add_employee'),
    path('delete_employee/<int:id>/', views.delete_employee, name='delete_employee'),
    path('edit_employee/<int:id>/', views.edit_employee, name='edit_employee'),
    path('userdata', views.user_data, name='userdata'),
    path('get_book_data/', views.get_book_data, name='get_book_data'),
    path('delete_book_data/', views.delete_book_data, name='delete_book_data'),

]