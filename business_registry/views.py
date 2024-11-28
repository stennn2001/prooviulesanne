from django.shortcuts import render
from .models import Company
from django.db.models import Q
from .forms import CompanyCreationForm, SearchForm
from django.shortcuts import redirect

# Create your views here.
def company_create(request):
    if request.method == "POST":
        form = CompanyCreationForm(request.POST)
        if form.is_valid():
            new_company = form.save()
            return redirect("company_detail", company_id=new_company.id)
    else:
        form = CompanyCreationForm()
    context = {
        "form": form
    }
    return render(request, 'business_registry/company_create.html', context)

def company_detail(request, company_id):
    company = Company.objects.get(pk=company_id)
    context = {
        "company": company
    }
    return render(request, 'business_registry/company_detail.html', context)

def search(request):
    form = SearchForm(request.GET or None)
    search_info = request.GET.get("search", "")
    print("KATSE1", search_info)
    if form.is_valid():
        search_info = form.cleaned_data.get("search", "")
        print("KATSE", search_info)
        companies_search = Company.objects.filter(Q(name__icontains=search_info) | Q(registration_code__icontains=search_info))
    else:
        companies_search = None
    print(companies_search)

    context = {
        "form": form,
        "search_info": search_info,
        "companies_search": companies_search
    }
    return render(request, 'business_registry/company_search.html', context)