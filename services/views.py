from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import DetailView, ListView

from .models import Service, Technology, Project


class JsonResponseMixin:
    @staticmethod
    def render_to_json_response(context, **response_kwargs):
        print(context)
        data = [{
            'name': project.name,
            'id': project.id,
            'img': project.get_technology_pic_url
        } for project in context['project_list']]

        has_next = context['page_obj'].has_next()

        context = {
            'has_next': has_next,
            'data': data
        }
        return JsonResponse(context, safe=False)


class TechnologyView(DetailView):
    template_name = 'technology.html'
    model = Technology

    context_object_name = 'tech'
    pk_url_kwarg = 'tech_id'

    def get_context_data(self, *args, **kwargs):
        from django.db import connection

        response = self.object

        context = {
            'tech_id': response.id,
            'name': response.name,
            'text': response.text,
            'subtechnologies': [*response.subtechnologies.values_list('name', flat=True)]
        }

        print('Technology', len(connection.queries))

        return context


class TechnologyApiView(JsonResponseMixin, ListView):
    paginate_by = 1
    pk_url_kwarg = 'tech_id'

    def get_queryset(self):
        tech_id = self.kwargs[self.pk_url_kwarg]
        tech = Technology.objects.get(pk=tech_id)
        return tech.project_set.order_by('id').all()

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


class ServicesView(ListView):
    template_name = 'services_overview.html'

    def get_queryset(self):
        return Service.objects.prefetch_related('technologies__subtechnologies').order_by('id')

    def get_context_data(self, *, object_list=None, **kwargs):
        from django.db import connection

        services = self.object_list

        data = [
            {'name': service.name,
             'technologies': [{
                 'id': tech.id,
                 'name': tech.name,
                 'sub_technologies': [{
                     'name': sub_tech.name
                 } for sub_tech in tech.subtechnologies.all()]
             } for tech in service.technologies.all()]
             } for service in services]

        context = {'services': data}

        print(len(connection.queries))
        return context


class AllProjectsApiView(JsonResponseMixin, ListView):
    paginate_by = 3

    def get_queryset(self):
        return Project.objects.order_by('id').only('id', 'name', 'technology_pic_link')

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


def all_projects(request):
    return render(request, 'all.html')


class ProjectView(DetailView):
    model = Project
    pk_url_kwarg = 'project_id'
    template_name = 'project.html'

    def get_context_data(self, **kwargs):
        from django.db import connection
        project_obj = self.object

        context = {
            'project_id': project_obj.id,
            'img': project_obj.get_project_pic_url,
            'name': project_obj.name,
            'project_tools': [*project_obj.projecttool_set.values_list('name', flat=True)],
            'text': project_obj.text
        }
        print(len(connection.queries))

        return context
