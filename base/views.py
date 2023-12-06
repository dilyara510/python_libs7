from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Task, Topic, Message, User
from .forms import TaskForm, UserForm, MyUserCreationForm, MessageForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# tasks = [
#     {'id': 1, 'name': 'Задание 1'},
#     {'id': 2, 'name': 'Задание 2'},
#     {'id': 3, 'name': 'Задание 3'},
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=email)
        except:
            messages.error(request, 'Пользователь не существует')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Некорректные логин или пароль!')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def registerPage(request):
    page= 'register'
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.role = 'user'
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Ошибка')

    return render(request, 'base/login_register.html',{'form':form})

def logoutUser(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    tasks = Task.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
    )
    
    
    topics = Topic.objects.all()
    task_count = tasks.count()
    task_messages = Message.objects.all().filter(Q(task__topic__name__icontains = q))

    context = {'tasks': tasks,'topics':topics,'task_count':task_count, 'task_messages':task_messages}
    return render(request, 'base/home.html', context)

@login_required(login_url='login')
def home(request):
    if request.user.role == 'user':
        q = request.GET.get('q') if request.GET.get('q') else ''
        tasks = Task.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )
        topics = Topic.objects.all()
        task_count = tasks.count()
        task_messages = Message.objects.all().filter(Q(task__topic__name__icontains=q))

        context = {'tasks': tasks, 'topics': topics, 'task_count': task_count, 'task_messages': task_messages}

        return render(request, 'base/home_user.html', context)
    elif request.user.role == 'admin':
        q = request.GET.get('q') if request.GET.get('q') else ''
        tasks = Task.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )
        topics = Topic.objects.all()
        task_count = tasks.count()
        task_messages = Message.objects.all().filter(Q(task__topic__name__icontains=q))

        context = {'tasks': tasks, 'topics': topics, 'task_count': task_count, 'task_messages': task_messages}
        return render(request, 'base/home.html', context)
    else:
        return redirect('login')


def task(request, pk):
    task = Task.objects.get(id=pk)
    task_messages = task.message_set.all().order_by('-created')
    participants = task.participants.all()
    
    user_message_count = 0
    for message in task_messages:
        if message.user == request.user:
            user_message_count += 1

    
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.task = task
            message.save()

            task.participants.add(request.user)
            success = True
        else:
            messages.error(request, 'Ошибка при отправке задания. Проверьте введенные данные.')

    else:
        form = MessageForm()

    context = {'task': task, 'task_messages': task_messages, 'participants': participants, 'form': form, 'user_message_count': user_message_count}
    return render(request, 'base/task.html', context)


def userProfile(request, pk):
    user = User.objects.get(id = pk)
    tasks = user.task_set.all()
    task_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'tasks': tasks,
               'task_messages': task_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url = 'login') 
def createTask(request):
    form=TaskForm()
    if request.method=='POST':
        form=TaskForm(request.POST)
        if form.is_valid():
            task=form.save(commit=False)
            task.host=request.user
            task.save()
            return redirect('home')
    context={'form':form}
    return render(request, 'base/task_form.html', context)

@login_required(login_url = 'login')
def updateTask(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    topics = Topic.objects.all()
    if request.user != task.host:
        return HttpResponse('Доступ запрещен!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        task.name = request.POST.get('name')
        task.topic = topic
        task.description = request.POST.get('description')
        task.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': task}
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


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Доступ запрещен!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})  
