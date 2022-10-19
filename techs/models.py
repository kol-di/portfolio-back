from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=200, unique=True)


class Technology(models.Model):
    name = models.CharField(max_length=200, unique=True)
    text = models.TextField()
    projects = models.ForeignKey(Project, on_delete=models.CASCADE, to_field='name')


