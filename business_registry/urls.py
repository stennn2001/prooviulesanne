from django.urls import path
from . import views


urlpatterns = [
# Company creation form
path("", views.company_create, name="company_create"),
# Company details
path("detail/<int:company_id>/", views.company_detail, name="company_detail"),
# Search
path("search/", views.search, name="search"),
]