from django.contrib import admin
from .models import task

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ['date_created', ]

admin.site.register(task, TaskAdmin)