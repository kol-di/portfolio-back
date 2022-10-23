from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from .models import Service, Technology, Project


def technology_api(request, tech_id):
    page_number = request.GET.get('page', 1)
    per_page = 1

    from django.db import connection

    technology = cache.get(f'technology{tech_id}')
    if technology is None:
        technology = Technology.objects.filter(id=tech_id)[0]
        cache.set(f'technology{tech_id}', technology, 60 * 15)

    print(len(connection.queries))
    paginator = Paginator(technology.project_set.order_by('id').all(), per_page)
    page_obj = paginator.get_page(page_number)
    print(len(connection.queries))

    data = [{'name': project.name,
             # 'img': project.technology_pic_link
             } for project in page_obj.object_list]

    print(len(connection.queries))

    payload = {
        'has_next': page_obj.has_next(),
        'data': data
    }
    return JsonResponse(payload)


def technology(request, tech_id):
    context = {'tech_id': tech_id}
    return render(request, 'technology.html', context)


def services_overview(request):
    services = Service.objects.prefetch_related('technologies__subtechnologies').order_by('id')

    from django.db import connection

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


# @cache_page(60 * 15)
def all_projects_api(request):
    page_number = request.GET.get('page', 1)
    per_page = 3

    from django.db import connection

    projects = cache.get('all_projects')
    if projects is None:
        projects = Project.objects.order_by('id').values_list('name', 'technology_pic_link')
        cache.set('all_projects', projects, 60 * 15)

    print(len(connection.queries))
    paginator = Paginator(projects, per_page)
    page_obj = paginator.get_page(page_number)
    print(len(connection.queries))

    data = [{'name': project_name,
             'img': img_link
             } for project_name, img_link in page_obj.object_list]

    print(len(connection.queries))

    payload = {
        'has_next': page_obj.has_next(),
        'data': data
    }
    return JsonResponse(payload)


def all_projects(request):
    return render(request, 'all.html')

