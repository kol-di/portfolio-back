from django.urls import path

from . import views

from .views import TechnologyView, TechnologyApiView


app_name = 'services'

urlpatterns = [
    path('', views.services_overview, name='services-overview'),
    path('technology/<int:tech_id>/', TechnologyView.as_view(), name='technology'),
    path('technology/api/<int:tech_id>', TechnologyApiView.as_view(), name='technology-api'),
    path('all_projects/', views.all_projects, name='all-projects'),
    path('all_projects/api', views.all_projects_api, name='all-projects-api'),
    path('all_projects/project/<int:project_id>', views.project, name='project'),
]
