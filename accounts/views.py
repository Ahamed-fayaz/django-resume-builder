from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from .forms import RegisterForm, LoginForm
# Create your views here.

def register(request):

    if request.user.is_authenticated:
        return redirect('resume_list')
        
    if request.method=='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form= RegisterForm()

    return render(request,'accounts/register.html',{"form":form})

def user_login(request):

    if request.user.is_authenticated:
        return redirect(resume_list)

    if request.method=='POST':
        loginform= LoginForm(request=request, data=request.POST)

        if loginform.is_valid():
            user= loginform.get_user()
            login(request,user)
            return redirect('resume_list')
    else:
        form= LoginForm()        
    return render(request,'accounts/login.html', {'form':form})

def user_logout(request):
    logout(request)
    return redirect('login')
