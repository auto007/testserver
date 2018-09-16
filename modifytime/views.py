from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request,'home.html')


def  my_login(request):
    if request.method == "POST":
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request,'error.html',{'message':'用户名和密码不正确'})
    return render(request, "login.html")
