from django.forms import ModelForm, ModelChoiceField, widgets
from django import forms
from . models import Task, User, Message, Topic
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    role = forms.CharField(widget=forms.HiddenInput(), initial='user')

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2', 'role']


class TaskForm(ModelForm):
    topic = ModelChoiceField(queryset=Topic.objects.all())
    class Meta:
        model = Task
        fields='__all__'
        exclude=['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body', 'attachment', 'rating']