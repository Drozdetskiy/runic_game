from django.urls import path
from django.views.generic import TemplateView

from runic_game_site.views import RegisterView, host

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='feed'),
    path('auth/register', RegisterView.as_view(), name='signup'),
    path('host', host, name='host'),
]
