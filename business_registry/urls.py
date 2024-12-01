from django.urls import path
from . import views


urlpatterns = [
    # Company creation form
    path("create/", views.company_create, name="company_create"),
    # Company details
    path("details/<int:company_id>/", views.company_detail, name="company_detail"),
    # Person details
    path("details/person/<int:person_id>/", views.person_detail, name="person_detail"),
    # Search
    path("search/", views.search, name="search"),
    # Company edit
    path("edit/<int:company_id>/", views.company_edit, name="company_edit"),
    
    # API Search
    path("shareholders/search/", views.search_shareholders, name="search_shareholders"),
]