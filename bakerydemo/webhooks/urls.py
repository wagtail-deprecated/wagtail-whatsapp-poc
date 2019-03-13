from django.urls import path
from django.views.decorators.cache import cache_page

from bakerydemo.webhooks.views import whatsapp

urlpatterns = [
    path('whatsapp/', whatsapp, name='whatsapp'),
]
