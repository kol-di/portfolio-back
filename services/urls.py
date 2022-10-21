from django.urls import path

from . import views

app_name = 'services'

urlpatterns = [
    path('', views.service_listing, name='listing'),
    path('listing_api/', views.listing_api, name='terms-api'),
    path('service/', views.service, name='service')
]
