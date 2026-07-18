from django.contrib import admin
from .models import JobParameter, Project

admin.site.register(Project)
admin.site.register(JobParameter)