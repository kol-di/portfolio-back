from django.contrib import admin

from .models import Service, Technology, Project

for model in [Service, Technology, Project]:
    admin.site.register(model)
