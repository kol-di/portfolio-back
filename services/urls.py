from django.urls import path

from . import views

from .views import TechnologyView, TechnologyApiView, ServicesView, AllProjectsApiView, ProjectView


app_name = 'services'

urlpatterns = [
    # path('', views.services_overview, name='services-overview'),
    path('', ServicesView.as_view(), name='services-overview'),
    path('technology/<int:tech_id>/', TechnologyView.as_view(), name='technology'),
    path('technology/api/<int:tech_id>', TechnologyApiView.as_view(), name='technology-api'),
    path('all_projects/', views.all_projects, name='all-projects'),
    # path('all_projects/api', views.all_projects_api, name='all-projects-api'),
    path('all_projects/api', AllProjectsApiView.as_view(), name='all-projects-api'),
    # path('all_projects/project/<int:project_id>', views.project, name='project'),
    path('all_projects/project/<int:project_id>', ProjectView.as_view(), name='project'),
]
