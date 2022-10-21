from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import Service


def service(request):
    return


def service_listing(request):
    services = Service.objects.values_list('name', flat=True)
    context = {'names': [service_name for service_name in services]}
    return render(request, 'load_more.html', context=context)


def listing_api(request):
    page_number = request.GET.get('page', 1)
    per_page = 1

    services = Service.objects.all().order_by('id')
    paginator = Paginator(services, per_page)
    page_obj = paginator.get_page(page_number)

    data = [{'name': obj.name,
             'technologies': [{
                 'name': tech.name,
                 'text': tech.text,
                 'projects': [{
                     'name': project.name
                     } for project in tech.project_set.all()]
                 } for tech in obj.technology_set.all()]
             }for obj in page_obj.object_list]

    payload = {
        'has_next': page_obj.has_next(),
        'data': data
    }
    return JsonResponse(payload)

