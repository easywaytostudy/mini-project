from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Book_Author(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    current_user = models.IntegerField()

    class Meta:
        db_table = 'bookauthor'
        verbose_name_plural = 'Book_Author'
        managed = True

    def __str__(self):
        return self.name


class Book(models.Model):
    book_title = models.CharField(max_length=30, blank=True, null=True)
    book_image = models.FileField(upload_to='image/book_image', null=True, blank=True,
                                  help_text="Upload only .png, .jpg & .jpeg image extension.")
    series = models.FloatField(blank=True, null=True)
    author_name = models.ForeignKey(Book_Author, blank=True, null=True, on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    pages = models.IntegerField(blank=True, null=True)
    current_user = models.IntegerField()

    class Meta:
        db_table = 'book'
        verbose_name_plural = 'Book'
        managed = True

    def __str__(self):
        return self.book_title


class Employee(models.Model):
    PROFILE_CHOICES = (
    ('Senior_Manager', 'Senior_Manager'), ('Junior_Manager', 'Junior_Manager'), ('Clerk', 'Clerk'), ('Guard', 'Guard'))
    employee_name = models.CharField(max_length=30, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    email = models.EmailField(max_length=30, null=True, blank=True)
    profile = models.CharField(max_length=20, choices=PROFILE_CHOICES)
    salary = models.IntegerField(null=True, blank=True)
    address = models.TextField(max_length=300, null=True, blank=True)
    current_user = models.IntegerField()

    class Meta:
        db_table = 'employee_record'
        verbose_name_plural = 'Employee'
        managed = True

    def __str__(self):
        return self.employee_name


class User_Data(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, )
    age = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'userdata'
        verbose_name_plural = 'User_Data'
        managed = True

    def __str__(self):
        return str(self.username)

# class UserProfile(models.Model):
#     user = models.OneToOneField(User)
#     activation_key = models.CharField(max_length=40, blank=True)
#     key_expires = models.DateTimeField()
#     is_active = models.BooleanField(default=False)

#     class Meta:
#     	db_table = 'userprofile'
#         verbose_name_plural = 'User profiles'
#         managed = True

#     def __str__(self):
#         return self.user.username
