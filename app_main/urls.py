from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

urlpatterns = [
    path("", views.home_page, name='home_page'),
    path(f"{_('our-services')}/", views.our_services, name='our_services'),
    path(f"{_('contacts')}/", views.contacts, name='contacts'),
    path(f"send-email/", views.send_email, name='send_email'),
    path("services/<slug:slug>/", views.service_detail, name='service_detail'),
    path("projects/<slug:slug>/", views.project_detail, name='project_detail'),
]
