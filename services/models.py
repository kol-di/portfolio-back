from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Technology(models.Model):
    name = models.CharField(max_length=200, unique=True)
    text = models.TextField(blank=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, related_name='technologies')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class SubTechnology(models.Model):
    name = models.CharField(max_length=200, unique=True)
    Technology = models.ForeignKey(Technology, on_delete=models.SET_NULL, null=True, related_name='subtechnologies')

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=200, unique=True)
    text = models.TextField(blank=True)
    project_pic_link = models.ImageField(blank=True, null=True, upload_to='project_imgs')
    technology_pic_link = models.ImageField(blank=True, null=True, upload_to='technology_imgs')
    technology = models.ManyToManyField(Technology)

    def __str__(self):
        return self.name

    @property
    def get_project_img_url(self):
        if self.project_pic_link and hasattr(self.project_pic_link, 'url'):
            return self.project_pic_link.url

    @property
    def get_technology_img_url(self):
        if self.technology_pic_link and hasattr(self.technology_pic_link, 'url'):
            return self.technology_pic_link.url

    class Meta:
        ordering = ['id']


class ProjectTool(models.Model):
    name = models.CharField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, related_name='project_tools')

    def __str__(self):
        return self.name




