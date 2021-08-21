from django.db import models
import re
import bcrypt

class Usersmanager(models.Manager):

    def register_validator (self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name must be at least 2 characters."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name must be at least 2 characters."
        email_regex = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['email']) == 0:
            errors['email'] = "You must enter an email"
        elif not email_regex.match(postData['email']):
            errors['email'] = "Must be a valid email"
        existing_users = Users.objects.filter(email=postData['email'])
        if len(existing_users) > 0:
            errors['exist'] = "This email is already in use"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        if postData['password'] != postData['passwordConfirm']:
            errors['notmatch'] = "Passwords do not match"
        return errors
    
    def login_validator(self, postData):
        errors = {}
        existing_user = Users.objects.filter(email=postData['email'])
        if len(postData['email']) == 0:
            errors['email'] = "Email must be entered"
        if len(existing_user) != 1:
            errors['email'] = "User does not exist."
        else:
            if len(postData['password']) < 8:
                errors['password'] = "Password must be at least 8 characters."
            elif bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()) != True:
                errors['mismatch'] = "Email and password not match."
        return errors

    def edit_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name must be at least 2 characters."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name must be at least 2 characters."
        email_regex = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['email']) == 0:
            errors['email'] = "You must enter an email"
        elif not email_regex.match(postData['email']):
            errors['email'] = "Must be a valid email"
        existing_users = Users.objects.filter(email=postData['email'])
        if len(existing_users) > 0:
            errors['exist'] = "This email is already in use"
        return errors

class Quotesmanager(models.Manager):

    def quote_validator(self, postData):
        errors = {}
        if len(postData['author']) < 4:
            errors['author'] = "Author must be more than 3 characters."
        if len(postData['quote_content']) < 10:
            errors['quote_content'] = "Quote must be at least 10 characters."
        return errors

class Users (models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = Usersmanager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Quotes (models.Model):
    quote_content = models.TextField()
    author = models.CharField(max_length=255)
    poster = models.ForeignKey(Users, related_name='User_quote', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = Quotesmanager()

class Like (models.Model):
    user = models.ForeignKey(Users, related_name='User_like', on_delete=models.CASCADE)
    quote = models.ForeignKey(Quotes, related_name='Quote_like', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)