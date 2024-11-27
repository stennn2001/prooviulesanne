from django.shortcuts import render
from business_registry.models import Company
from django.db.models import Q

def home(request):
    return render(request, 'business_registry/home.html')

def search(request):
    search_info = request.GET.get("search", "")
    print("KATSE", search_info)
    companies_search = Company.objects.filter(Q(name__icontains=search_info) | Q(registration_code__icontains=search_info))
    print(companies_search)

    context = {
        "search_info": search_info,
        "companies_search": companies_search
    }
    return render(request, 'business_registry/company_search.html', context)

def company_detail(request, company_id):
    company = Company.objects.get(pk=company_id)
    context = {
        "company": company
    }
    return render(request, 'business_registry/company_detail.html', context)