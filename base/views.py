from django.shortcuts import render, redirect
from .models import Task 
from .forms import TaskForm

# tasks = [
#     {'id': 1, 'name': 'Задание 1'},
#     {'id': 2, 'name': 'Задание 2'},
#     {'id': 3, 'name': 'Задание 3'},
# ]


def home(request):
    tasks=Task.objects.all()
    context = {'tasks': tasks}
    return render(request, 'base/home.html', context)


def task(request, pk):
    task = Task.objects.get(id=pk)
    context = {'task': task}
    return render(request, 'base/task.html', context)


# def task(request,pk):
#     return render(request,'base/task.html')

def createTask(request):
    form=TaskForm()
    if request.method=='POST':
        form=TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request, 'base/task_form.html', context)


def updateTask(request, pk):
    task=Task.objects.get(id=pk)
    form=TaskForm(instance=task)

    if request.method=='POST':
        form=TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context={'form':form}

    return render(request, 'base/task_form.html', context)

def deleteTask(request,pk):
    task=Task.objects.get(id=pk)
    if request.method=='POST':
        task.delete()
        return redirect('home')

    return render(request, 'base/delete.html',{'obj':task} )