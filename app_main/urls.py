from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_page),
    path("<slug:slug>/", views.service_detail, name='service_detail'),
]
