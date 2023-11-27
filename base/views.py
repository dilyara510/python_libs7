from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Task, Topic
from .forms import TaskForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# tasks = [
#     {'id': 1, 'name': 'Задание 1'},
#     {'id': 2, 'name': 'Задание 2'},
#     {'id': 3, 'name': 'Задание 3'},
# ]

def loginPage(request):
    # page = 'login'
    # if request.user.is_authenticated:
    #     return redirect('home')

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {}
    return render(request, 'base/login_register.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''

    tasks = Task.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    
    
    topics=Topic.objects.all()
    task_count=tasks.count()
    context = {'tasks': tasks,'topics':topics,'task_count':task_count}
    return render(request, 'base/home.html', context)


def task(request, pk):
    task = Task.objects.get(id=pk)
    context = {'task': task}
    return render(request, 'base/task.html', context)


# def task(request,pk):
#     return render(request,'base/task.html')

@login_required(login_url='login') 
def createTask(request):
    form=TaskForm()
    if request.method=='POST':
        form=TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request, 'base/task_form.html', context)

@login_required(login_url='login') 
def updateTask(request, pk):
    task=Task.objects.get(id=pk)
    form=TaskForm(instance=task)

    if request.user!=task.host:
        return HttpResponse('Доступ запрещен!')
    
    if request.method=='POST':
        form=TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context={'form':form}

    return render(request, 'base/task_form.html', context)

@login_required(login_url='login') 
def deleteTask(request,pk):
    task=Task.objects.get(id=pk)

    if request.user!=task.host:
        return HttpResponse('Доступ запрещен!')
    if request.method=='POST':
        task.delete()
        return redirect('home')

    return render(request, 'base/delete.html',{'obj':task} )