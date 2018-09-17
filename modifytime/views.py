from django.shortcuts import render,redirect,HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import LoginForm,RegForm
import time
import os
import json
import subprocess

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

@login_required
def logout(request):
    auth.logout(request)
    return redirect("/login")

@login_required
def home(request):
    ser_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # return HttpResponse(ser_time)
    time_context_dict = {'ht_time': ser_time}
    if request.method == "POST":
        time_from_txt_dict = json.load(open('result.txt', 'r'))
        time_from_txt = time_from_txt_dict['usertime']
        receive_time_dict = request.POST
        receive_time = receive_time_dict['usertime']
        if receive_time :
            if receive_time != time_from_txt :
                print(receive_time)
                print('正常执行')
                json.dump(receive_time_dict, open('result.txt', 'w'))
                os.environ['shell_change_time'] = receive_time
                os.system('sh /data/yunwei/testserver/changtime.sh "${shell_change_time}"')
                return redirect('/result/')

    return render(request,'modifytime.html',time_context_dict)

@login_required
def result(request):
    return HttpResponse('修改成功!  <a href="/" >返回主页</a>')

@login_required
def correcttime(request):
    ret=''
    myarg = request.GET.get('action')
    if myarg == 'xgsj':
        p = subprocess.Popen("/usr/sbin/ntpdate ntp.ksyun.cn", shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        p.wait()
        ser_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        ret = "时间已经校准！当前正确时间：%s" %ser_time

    return render(request, 'correcttime.html', {'ret': ret})
