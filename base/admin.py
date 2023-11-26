from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.

from .models import Task,Topic,Message
# , Topic, Message, User

admin.site.register(Task)
admin.site.register(Topic)
admin.site.register(Message)
