from django.urls import path
from . import views


urlpatterns = [
path("", views.company_create, name="company_create"),
path("", views.person, name="person"),
]