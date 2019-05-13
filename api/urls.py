from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import my_first_api_view

urlpatterns = [
    path('', my_first_api_view, name='first-api'),
]
