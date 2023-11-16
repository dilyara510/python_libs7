from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('task/<str:pk>/', views.task, name="task"),
]