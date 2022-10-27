from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.core.cache import cache

from .models import Service, Technology, Project


def technology_api(request, tech_id):
    page_number = request.GET.get('page', 1)
    per_page = 1

    from django.db import connection

    tech = cache.get(f'technology{tech_id}')
    if tech is None:
        tech = Technology.objects.get(pk=tech_id)
        cache.set(f'technology{tech_id}', tech, 60 * 15)

    print('TEchnology API', len(connection.queries))
    paginator = Paginator(tech.project_set.order_by('id').all(), per_page)
    page_obj = paginator.get_page(page_number)
    print('TEchnology API', len(connection.queries))

    data = [{'name': project.name,
             'id': project.id,
             'img': project.get_technology_pic_url
             } for project in page_obj.object_list]

    print('TEchnology API', len(connection.queries))

    payload = {
        'has_next': page_obj.has_next(),
        'data': data
    }
    return JsonResponse(payload)


def technology(request, tech_id):
    from django.db import connection
    tech = Technology.objects.get(pk=tech_id)

    context = {
        'tech_id': tech_id,
        'name': tech.name,
        'text': tech.text,
        'subtechnologies': [*tech.subtechnologies.values_list('name', flat=True)]
    }

    print('Technology', len(connection.queries))
    return render(request, 'technology.html', context)


def services_overview(request):
    services = Service.objects.prefetch_related('technologies__subtechnologies').order_by('id')

    from django.db import connection
    print(len(connection.queries))

    data = cache.get('services_overview')
    if data is None:
        data = [{'name': service.name,
                 'technologies': [{
                     'id': tech.id,
                     'name': tech.name,
                     'sub_technologies': [{
                         'name': sub_tech.name
                         } for sub_tech in tech.subtechnologies.all()]
                     } for tech in service.technologies.all()]
                 } for service in services]
        cache.set('services_overview', data, 60 * 15)

    print(len(connection.queries))

    context = {'services': data}

    return render(request, 'services_overview.html', context)


def all_projects_api(request):
    page_number = request.GET.get('page', 1)
    per_page = 3

    from django.db import connection

    projects = cache.get('all_projects')
    if projects is None:
        projects = Project.objects.order_by('id').values_list('id', 'name', 'technology_pic_link')
        cache.set('all_projects', projects, 60 * 15)

    print(len(connection.queries))
    paginator = Paginator(projects, per_page)
    page_obj = paginator.get_page(page_number)
    print(len(connection.queries))

    data = [{'id': project_id,
             'name': project_name,
             'img': img_link
             } for project_id, project_name, img_link in page_obj.object_list]

    print(len(connection.queries))

    payload = {
        'has_next': page_obj.has_next(),
        'data': data
    }
    return JsonResponse(payload)


def all_projects(request):
    return render(request, 'all.html')


def project(request, project_id):
    from django.db import connection

    project_obj = Project.objects.defer('technology_pic_link').get(pk=project_id)

    context = {
        'project_id': project_obj.id,
        'img': project_obj.get_project_pic_url,
        'name': project_obj.name,
        'project_tools': [*project_obj.projecttool_set.values_list('name', flat=True)],
        'text': project_obj.text
    }

    print(len(connection.queries))
    print(*project_obj.projecttool_set.values_list('name', flat=True))

    return render(request, 'project.html', context)




