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
    text = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=200, unique=True)
    project = models.ForeignKey(Technology, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name




