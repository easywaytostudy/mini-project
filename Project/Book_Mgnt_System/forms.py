from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Book, Book_Author, Employee, User_Data
from django.contrib.auth.forms import AuthenticationForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter username', 'autofocus': '', }),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name', }),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name', }),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email', }),
        }


class LoginForm(AuthenticationForm):
    class Meta:
        widgets = {

        }


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('book_title', 'book_image', 'series', 'author_name', 'description', 'pages')

        widgets = {
            'book_title' : forms.TextInput(attrs={'class' :'form-control' ,'required' :True, 'autofocus' :''}),
            'book_image'	: forms.FileInput(attrs={'class' :'form-control' ,'multiple': True, 'accept' :'image/*'}),
            'series'	 	: forms.NumberInput(attrs={'class' :'form-control' ,'required' :True}),
            'description'	: forms.Textarea(attrs={'class' :'form-control' ,'required' :True}),
            'pages'		 	: forms.NumberInput(attrs={'class' :'form-control' ,'required' :True}),
        }


class BookAuthorForm(forms.ModelForm):
    class Meta:
        model = Book_Author
        fields = ('name',)
        widgets = {
            'name' : forms.TextInput
            (attrs={'class':'form-control', 'required':True, 'autofocus':'', 'placeholder':'Author name'})
        }


class UpdateBookForm(forms.ModelForm):
    class Meta:
        model 	= Book
        fields 	= ('book_title', 'series', 'description', 'pages')

        widgets = {
            'book_title' 	: forms.TextInput(attrs={'class':'form-control' ,'autofocus':''}),
            'series'	 	: forms.NumberInput(attrs={'class':'form-control'}),
            'description'	: forms.Textarea(attrs={'class':'form-control'}),
            'pages'		 	: forms.NumberInput(attrs={'class':'form-control'}),

        }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ('employee_name', 'age', 'email', 'profile', 'salary', 'address')
        widgets = {
            'employee_name' : forms.TextInput(attrs={'class':'form-control' ,'autofocus':'' ,
                                                     'placeholder':'Employee name', 'required':True}),
            'age' 			: forms.NumberInput(attrs={'class':'form-control' ,'placeholder':'Employee age',
                                                        'required':True}),
            'email' 		: forms.EmailInput(attrs={'class':'form-control' ,'placeholder':'Employee email' ,}),
            'salary'        : forms.NumberInput(attrs={'class':'form-control' ,'placeholder':'Employee salary',
                                                       'required':True ,}),
            'address' 		: forms.Textarea(attrs={'class':'form-control' ,'placeholder':'Employee address',
                                                     'required':True}),
        }


class UpdateEmployeeForm(forms.ModelForm):
    class Meta:
        model 	= Employee
        fields 	= ('employee_name', 'age', 'email', 'profile', 'salary', 'address')
        widgets = {

            'employee_name' : forms.TextInput(attrs={'class':'form-control', 'autofocus':'', }),
            'age' 			: forms.NumberInput(attrs={'class':'form-control'}),
            'email' 		: forms.EmailInput(attrs={'class':'form-control'}),
            'salary'        : forms.NumberInput(attrs={'class':'form-control'}),
            'address' 		: forms.Textarea(attrs={'class':'form-control'}),
        }


class UserDataForm(forms.ModelForm):
    class Meta:
        model 	= User_Data
        fields 	= ('username', 'age')
        widgets = {

            'age': forms.NumberInput(attrs={'class':'form-control'})
        }