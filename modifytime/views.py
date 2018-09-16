from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import LoginForm,RegForm

@login_required
def home(request):
    return render(request,'home.html')

def my_login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request,user)
            return redirect('/')
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, "login.html",context)

def register(request):
    if request.method == "POST":
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            password = reg_form.cleaned_data['password']
            user = User.objects.create_user(username,'',password)
            user.save()
            #注册完成后登录
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect('/')
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, "register.html",context)
