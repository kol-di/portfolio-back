from django.db import models
from techs.models import Technology


class Service(models.Model):
    name = models.CharField(max_length=200, unique=True)
    technologies = models.ForeignKey(Technology, on_delete=models.CASCADE)

