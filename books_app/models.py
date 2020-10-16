from django.db import models
import re 

class UserManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        if postData['password'] != postData['password_confirmation']:
            errors['password_confirmation'] = "Passwords do not match"
        return errors
    
class BookManager(models.Manager):
    def basic_validator(self,postData):
        errors = {}
        if len(postData['title']) < 1:
            errors['title'] = "Title field is required"
        if len(postData['description']) < 5 and len(postData['description']) > 0:
            errors['description'] = "Description should be at least 5 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    uploaded_by = models.ForeignKey(User,related_name="books_uploaded",on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User,related_name="users")
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    objects = BookManager()