from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index (request):
    return render (request, 'index.html')

def register(request):
    errors = Users.objects.register_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = Users.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            )
        request.session['user_id'] = user.id
        request.session['username'] = user.first_name
        return redirect('/success')


def login(request):
    errors = Users.objects.login_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = Users.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        request.session['username'] = user.first_name
        return redirect('/success')

def success (request):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        context = {
            "all_quotes":Quotes.objects.all(),
        }
    return render (request, 'quotes.html', context)

def addquote (request):
    if request.method != 'POST':
        return redirect ('/success')
    else:
        errors = Quotes.objects.quote_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
        else:
            newquote = Quotes.objects.create(
                quote_content = request.POST['quote_content'],
                author = request.POST['author'],
                poster = Users.objects.get(id = request.session['user_id']),
                
            )
        return redirect('/success')

def userprofile(request, user_id):
    this_user = Users.objects.get(id = user_id)
    context = {
        "user":this_user,
        "this_user_quotes": Quotes.objects.filter(poster = this_user)
    }
    return render (request, 'userquotes.html', context)

def editaccount (request,user_id):
    context = {
        'user': Users.objects.get(id = user_id)
    }
    return render (request, 'editaccount.html', context)

def like(request, quote_id):
    created = Like.objects.get_or_create(user_id=request.session['user_id'], quote_id=quote_id)
    if not created:
        return redirect ('/success')
    else:
        return redirect ('/success')

def updateuserprofile(request, user_id):
    if request.method != 'POST':
        return redirect ('/success')
    else:
        errors = Users.objects.edit_validator(request.POST)
        this_user = Users.objects.get(id = user_id)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect (f'/myaccount/{this_user.id}')
        else:
            this_user = Users.objects.get(id = user_id)
            this_user.first_name = request.POST['first_name']
            this_user.last_name = request.POST['last_name']
            this_user.email = request.POST['email']
            this_user.save()
            return redirect (f'/user/{this_user.id}')

def delete(request, quote_id):
    this_quote = Quotes.objects.filter(id = quote_id)
    this_quote.delete()
    return redirect ('/success')

def logout (request):
    request.session.flush()
    return redirect('/')
