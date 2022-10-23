from django.contrib import admin

from .models import Service, Technology, SubTechnology, Project, ProjectTool


class TechnologyAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class ProjectAdmin(admin.ModelAdmin):
    # raw_id_fields = ("technology", )
    autocomplete_fields = ('technology',)


for model in [Service, SubTechnology, ProjectTool]:
    admin.site.register(model)

admin.site.register(Technology, TechnologyAdmin)
admin.site.register(Project, ProjectAdmin)


