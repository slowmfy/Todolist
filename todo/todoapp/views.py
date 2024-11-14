from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import todo
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def home(request):
    if request.method == 'POST':
        
        task = request.POST.get('task')
        new_todo = todo(user=request.user, todo_name=task)
        new_todo.save()

    # This code should be outside the 'if' block so that it runs for both GET and POST requests
    all_todos = todo.objects.filter(user=request.user)  # Get all items
    context = {'todos': all_todos} 
# This is always defined
    
    return render(request, 'todoapp/todo.html', context)
 #rquest.user = crrent user using the website
  #get all items

def register(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':

        
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if len(password)< 3:
            messages.error(request,'passoword must be at least 3 characters')
            return redirect('register')
        
        get_all_user_by_username = User.objects.filter(username=username)
        if get_all_user_by_username:
            
            messages.error(request,'Error,Username already exists,use another')
            return redirect('register')
            
            
        
        new_user=User.objects.create_user(username=username,email=email,password=password)
        new_user.save()
        messages.success(request,'user successfully created ,login now')
        return redirect('login')
        
    
    return render(request,'todoapp/register.html',{})


def loginpage(request):
    
    if request.user.is_authenticated:
        return redirect('home-page')
    
    
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        validate_user=authenticate(username=username,password=password)
        if validate_user is not None:
            login(request,validate_user)
            return redirect('home-page')
        else:
            messages.error(request,'Error,User Details o user does not eixsts')
            return redirect('login')
            
            
        
    
    
    return render(request,'todoapp/login.html',{})
def LogoutView(request):
    logout(request)
    return redirect('login')


@login_required
def DeleteTask(request, name):
    get_todo=todo.objects.get(user=request.user,todo_name=name)
    get_todo.delete()
    return redirect('home-page')
@login_required
def Update(request,name):
    get_todo=todo.objects.get(user=request.user,todo_name=name)
    get_todo.status = True
    get_todo.save()
    return redirect('home-page')
    