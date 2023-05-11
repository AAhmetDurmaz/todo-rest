from django.contrib import admin
from .models import Task, TaskList, User

admin.site.register(Task)
admin.site.register(TaskList)
admin.site.register(User)