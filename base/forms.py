from django.forms import ModelForm
from .models import Task
from django.contrib.auth.models import User

class TaskForm(ModelForm):
    class Meta:
        model=Task
        fields='__all__'
        exclude=['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model=User
        fields=['username','email']