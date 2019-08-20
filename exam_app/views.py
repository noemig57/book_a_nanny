from django.shortcuts import render, redirect
from .models import *
from .models import Book

import bcrypt
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user_matches = User.objects.filter(email=request.POST['email'])
        if len(user_matches) > 0:
            messages.error(request, 'Email already exists. Please log in.')
            return redirect('/')
        else:
            User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=request.POST['password']
            )
            last_user_created = User.objects.last()
            request.session['user_id'] = last_user_created.id
            request.session['user_name'] = last_user_created.first_name
            messages.success(request, 'Successfully registered!')
            return redirect('/dash')

def dash(request):
    user= User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'all_books': Book.objects.all()
    }
    return render(request, 'dash.html', context)

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user_to_login_list = User.objects.filter(email=request.POST['login_email'])
        request.session['user_id'] = user_to_login_list[0].id
        request.session['user_name'] = user_to_login_list[0].first_name
        messages.success(request, 'Successfully logged in!')
        return redirect('/dash')

def book(request):
    return render(request, 'book.html')

def new_book_process(request):
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/book/new')
    else:
        user = User.objects.get(id = request.session['user_id'])
        Book.objects.create(address=request.POST['address'], phone=request.POST['phone'], start=request.POST['start'], end=request.POST['end'], notes=request.POST['notes'], creator=user)
        print (Book.objects.all())
    return redirect(f"/dash")

def edit_book(request, bookid):
    book = Book.objects.get(id=bookid)
    user = User.objects.get(id = request.session['user_id'])
    context={
        'user': user,
        "book": book
    }
    return render(request, 'edit.html', context)

def edit_book_process(request, bookid):
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/book/edit/{bookid}')
    else:
        book= Book.objects.get(id=bookid)
        book.phone=request.POST['phone']
        book.address=request.POST['address']
        book.start=request.POST['start']
        book.end=request.POST['end']
        book.plan= request.POST['notes']
        book.save()
        return redirect(f"/dash")

def add_book(request):
    errors = User.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/book')
    else:
        user = User.objects.get(id = request.session['user_id'])
        Job.objects.create(title=request.POST['title'], desc=request.POST['desc'], location=request.POST['location'], creator=user)
        print (Job.objects.all())
    return redirect(f"/dash")


def view_book(request, bookid):
    user= User.objects.get(id=request.session['user_id'])
    book= Book.objects.get(id=bookid)
    context = {
        'user': user,
        'book': book
    }
    return render(request, 'view.html', context)


def delete(request, bookid):
    book= Book.objects.get(id=bookid)
    book.delete()
    return redirect('/dash')


def profile(request, userid):
    user = User.objects.get(id=userid)
    context = {
        "user": user
    }
    return render(request, "profile.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')

