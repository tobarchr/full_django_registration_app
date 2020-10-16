from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request,'index.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if request.method == "POST":
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            hash_key = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            User.objects.create(first_name = request.POST['first_name'],last_name = request.POST['last_name'],email=request.POST['email'],password=hash_key)
            return redirect ('/books')
    else:
        return redirect ('/')
def login(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(),logged_user.password.encode()):
                request.session['user'] = logged_user.id 
                return redirect('/books')
        return redirect('/')
    return redirect('/')

def books(request):
    user_id = request.session['user']
    context ={
        "all_books" : Book.objects.all(),
        "user_info" : User.objects.get(id=user_id),
        "favorites" : User.objects.get(id=user_id).users.all()
    }
    return render (request,'books.html',context)

def book_details(request,book_id):
    user_id = request.session['user']
    user_info = User.objects.get(id=user_id)
    book_info = Book.objects.get(id=book_id)
    context = {
        'user_info' : user_info,
        'book_info' : book_info
    }
    return render(request,'book_details.html',context)

def add_book(request):
    errors = Book.objects.basic_validator(request.POST)
    if request.method == "POST":
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect('/books')
        else:
            user_id = request.session['user']
            Book.objects.create(title=request.POST['title'],description=request.POST['description'],uploaded_by=User.objects.get(id=user_id))
            added_book = Book.objects.last()
            upload_user_id = User.objects.get(id=user_id)
            upload_user_id.users.add(added_book)
            return redirect('/books')
    else:
        return redirect ('/books')

def update_book(request,book_id):
    if request.method == "POST":
        errors = Book.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value)
                return redirect('/books/'+str(book_id))
        else:
            user_id = request.session['user']
            book_to_update = Book.objects.get(id=book_id)
            book_to_update.description = request.POST['description']
            book_to_update.title = request.POST['title']
            book_to_update.save()
            return redirect('/books/'+str(book_id))
    else:
        return redirect('/books/'+str(book_id))

def delete_book(request,book_id):
    book_to_delete = Book.objects.get(id=book_id)
    book_to_delete.delete()
    return redirect('/books')

def log_off(request):
    del request.session['user']
    return redirect ('/')

def add_to_favorite(request,book_id):
    user_adding = User.objects.get(id=request.session['user'])
    book_to_favorites = Book.objects.get(id=book_id)
    book_to_favorites.users_who_like.add(user_adding)
    return redirect('/books/'+str(book_id))

def remove_favorite(request,book_id):
    user_removing = User.objects.get(id=request.session['user'])
    book_to_favorites = Book.objects.get(id=book_id)
    book_to_favorites.users_who_like.remove(user_removing)
    return redirect('/books/'+str(book_id))


