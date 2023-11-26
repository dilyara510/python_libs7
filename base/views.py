from django.shortcuts import render
from .models import Task 

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