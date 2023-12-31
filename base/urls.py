from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('register/', views.registerPage, name="register"),


    path('', views.home, name="home"),
    path('task/<str:pk>/', views.task, name="task"),

    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-task/', views.createTask, name="create-task"),
    path('update-task/<str:pk>/', views.updateTask, name="update-task"),
    path('delete-task/<str:pk>/', views.deleteTask, name="delete-task"),

    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('rate_message/<int:pk>/', views.rate_message, name='rate-message'),

    path('update-user/', views.updateUser, name="update-user"),
]