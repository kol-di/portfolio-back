from django.shortcuts import render
from rest_framework import generics, serializers, permissions
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

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
        return obj.get_technology_img_url


class AllProjectsSerializer(ProjectSerializer):
    class Meta(ProjectSerializer.Meta):
        fields = ['id', 'name', 'project_img_url']


class OverviewProjectSerializer(ProjectSerializer):
    class Meta(ProjectSerializer.Meta):
        fields = ['id', 'name', 'text', 'project_img_url', 'project_tools']


class SubtechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTechnology
        fields = ['name']


class TechnologySerializer(serializers.ModelSerializer):
    subtechnologies = SubtechnologySerializer(many=True, read_only=True)

    class Meta:
        model = Technology
        fields = ['id', 'name', 'text', 'subtechnologies']


class ServiceSerializer(serializers.ModelSerializer):
    technologies = TechnologySerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'name', 'technologies']


class TechnologyView(RetrieveAPIView):
    """
    Renders base for Technology page "technology.html".
    Accepts tech_id as a part of url.
    """
    template_name = 'technology.html'
    lookup_url_kwarg = 'tech_id'
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer


class TechnologyPagination(PageNumberPagination):
    page_size = 1


class TechnologyApiView(ListAPIView):
    """
    Returns paginated responses with projects, related
    to the given technology.

    Accepts tech_id as a part of url.
    Accepts "page" url parameter.

    Returns JSON.
    """
    renderer_classes = [JSONRenderer]
    pagination_class = TechnologyPagination
    lookup_url_kwarg = 'tech_id'
    serializer_class = OverviewProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(technology__id=self.kwargs.get(self.lookup_url_kwarg)).all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class ServicesView(ListAPIView):
    """
    Renders page with all services list "services_overview.html".
    """
    template_name = 'services_overview.html'
    serializer_class = ServiceSerializer
    queryset = Service.objects.prefetch_related('technologies__subtechnologies')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response({'services': serializer.data})


class AllProjectsPagination(PageNumberPagination):
    page_size = 3


class AllProjectsApiView(ListAPIView):
    """
    Returns paginated results with list of all projects.

    Accept "page" url parameter.

    Returns JSON.
    """
    pagination_class = AllProjectsPagination
    renderer_classes = [JSONRenderer]
    serializer_class = AllProjectsSerializer

    queryset = Project.objects.all()


@api_view(http_method_names=['GET'])
@permission_classes((permissions.AllowAny, ))
def all_projects(request):
    """
    Renders base for page with all projects "all.html".
    """
    return render(request, 'all.html')


class ProjectView(RetrieveAPIView):
    """
    Renders page of a certain project "project.html".

    Accepts "project_id" as a part of url.
    """
    serializer_class = OverviewProjectSerializer
    queryset = Project.objects.all()
    lookup_url_kwarg = 'project_id'
    template_name = 'project.html'

