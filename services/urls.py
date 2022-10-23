from django.urls import path

from . import views

app_name = 'services'

urlpatterns = [
    path('', views.services_overview, name='services-overview'),
    path('technology/<int:tech_id>/', views.technology, name='technology'),
    path('technology/api/<int:tech_id>', views.technology_api, name='technology-api'),
    path('all_projects/', views.all_projects, name='all-projects'),
    path('all_projects/api', views.all_projects_api, name='all-projects-api')
]
