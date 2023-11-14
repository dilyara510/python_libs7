from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse('Home page')

def task(request):
    return HttpResponse('TASK')