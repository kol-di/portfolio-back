from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import DetailView, ListView
from rest_framework import generics, serializers
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from .models import Service, Technology, Project, SubTechnology


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'text', 'project_img_url', 'technology_img_url', 'project_tools']

    project_tools = serializers.StringRelatedField(many=True)
    if 'project_img_url' in Meta.fields:
        project_img_url = serializers.SerializerMethodField('_get_alternate_project_img')
    if 'technology_img_url' in Meta.fields:
        technology_img_url = serializers.SerializerMethodField('_get_alternate_tech_img')

    def _get_alternate_project_img(self, obj):
        return obj.get_project_img_url

    def _get_alternate_tech_img(self, obj):
        return getattr(obj, 'get_technology_img_url', None)


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


class SubtechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTechnology
        fields = ['name']


class TechnologySerializer(serializers.ModelSerializer):
    subtechnologies = SubtechnologySerializer(many=True, read_only=True)

    class Meta:
        model = Technology
        fields = ['id', 'name', 'subtechnologies']


class ServiceSerializer(serializers.ModelSerializer):
    technologies = TechnologySerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'name', 'technologies']


class ServicesView(ListAPIView):
    template_name = 'services_overview.html'
    serializer_class = ServiceSerializer
    queryset = Service.objects.prefetch_related('technologies__subtechnologies')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response({'services': serializer.data})


class AllProjectsSerializer(ProjectSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'project_img_url']


class AllProjectsPagination(PageNumberPagination):
    page_size = 3


class AllProjectsApiView(ListAPIView):
    pagination_class = AllProjectsPagination
    renderer_classes = [JSONRenderer]
    serializer_class = AllProjectsSerializer

    queryset = Project.objects.all()


def all_projects(request):
    return render(request, 'all.html')


class OverviewProjectSerializer(ProjectSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'text', 'project_img_url', 'project_tools']


class ProjectView(RetrieveAPIView):
    serializer_class = OverviewProjectSerializer
    queryset = Project.objects.all()
    lookup_url_kwarg = 'project_id'
    template_name = 'project.html'

