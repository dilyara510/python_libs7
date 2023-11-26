from django.shortcuts import render


tasks = [
    {'id': 1, 'name': 'Задание 1'},
    {'id': 2, 'name': 'Задание 2'},
    {'id': 3, 'name': 'Задание 3'},
]


def home(request):
    context = {'tasks': tasks}
    return render(request, 'base/home.html', context)


def task(request, pk):
    task = None
    for i in tasks:
        if i['id'] == int(pk):
            task = i
    context = {'task': task}
    return render(request, 'base/task.html', context)


# def task(request,pk):
#     return render(request,'base/task.html')