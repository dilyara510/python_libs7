from django.contrib import admin

# Register your models here.
<<<<<<< HEAD
=======
from django.contrib import admin

# Register your models here.

from .models import Task,Topic,Message,User

admin.site.register(User)
admin.site.register(Task)
admin.site.register(Topic)
admin.site.register(Message)
>>>>>>> 52cbfbd74f821ccddb3502551a7f68197e596d39
