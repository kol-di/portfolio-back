from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    # @staticmethod
    # def service_name2template(name):
    #     return f'{name}.html'


class Technology(models.Model):
    name = models.CharField(max_length=200, unique=True)
    text = models.TextField(blank=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, related_name='technologies')

    def __str__(self):
        return self.name


class SubTechnology(models.Model):
    name = models.CharField(max_length=200, unique=True)
    Technology = models.ForeignKey(Technology, on_delete=models.SET_NULL, null=True, related_name='subtechnologies')

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=200, unique=True)
    text = models.TextField(blank=True)
    project_pic_link = models.FileField(blank=True, null=True)
    technology_pic_link = models.FileField(blank=True, null=True)
    technology = models.ManyToManyField(Technology)

    def __str__(self):
        return self.name


class ProjectTool(models.Model):
    name = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name




