from django.shortcuts import render
from .models import Company, Shareholder, Person
from django.http import JsonResponse
from django.db.models import Q
from .forms import CompanyCreationForm, SearchForm, ShareholderEditForm
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.forms import modelformset_factory
from django.contrib import messages

# Create your views here.
def company_create(request):
    print("KATSE", request.POST)
    
    shareholders_json_errors = []

    if request.method == "POST":
        shareholders_json_value = request.POST.get('shareholders_json', '').strip()
        if not shareholders_json_value:
            shareholders_json_errors.append("Shareholders cannot be empty.")
        form = CompanyCreationForm(request.POST)
        if form.is_valid():
            new_company = form.save()
            return redirect("company_detail", company_id=new_company.id)
    else:
        form = CompanyCreationForm()
    context = {
        "form": form,
        "shareholders_json_errors": shareholders_json_errors
    }
    return render(request, 'business_registry/company_create.html', context)

def company_detail(request, company_id):
    company = Company.objects.get(pk=company_id)
    context = {
        "company": company,
    }
    return render(request, 'business_registry/company_detail.html', context)

def search(request):
    form = SearchForm(request.GET or None)
    search_info = request.GET.get("search", "")
    
    if form.is_valid():
        search_info = form.cleaned_data.get("search", "")
        companies_search = Company.objects.filter(Q(name__icontains=search_info) | Q(code__icontains=search_info))
        length_companies_search = len(companies_search)
        if companies_search:
            messages.success(request, f"Success, found {length_companies_search} {'matches' if length_companies_search != 1 else 'match'}.") 
        else:
            messages.info(request, "No search results")
    else:
        companies_search = None

    context = {
        "form": form,
        "search_info": search_info,
        "companies_search": companies_search
    }
    return render(request, 'business_registry/company_search.html', context)

def search_shareholders(request):
    search_phrase = request.GET.get("search", "").strip()
    
    if search_phrase:
        company_results = Company.objects.filter(
            Q(name__icontains=search_phrase) | Q(code__icontains=search_phrase)
        ).values("id", "name", "code")
        person_results = Person.objects.filter(
            Q(first_name__icontains=search_phrase) | Q(last_name__icontains=search_phrase) | Q(code__icontains=search_phrase)
            ).values("id", "first_name", "last_name", "code")
        
        for company in company_results:
            company["type"] = "company"
        for person in person_results:
            person["type"] = "person"
            
        shareholders = list(company_results) + list(person_results)
    else:
        shareholders = []

    return JsonResponse({
        "shareholders": shareholders
    })

def company_edit(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    shareholders = company.shareholder.all()
    print(shareholders)
    ShareholderFormSet = modelformset_factory(Shareholder, form=ShareholderEditForm, extra=0)
    if request.method == 'POST':
        form = ShareholderEditForm(request.POST, instance=shareholders)
        formset = ShareholderFormSet(request.POST, queryset=company.shareholder.all())
        if form.is_valid():
            form.save()
            return redirect('company_detail', company_id=company.id)
    else:
        form = ShareholderEditForm(instance=company)
        formset = ShareholderFormSet(queryset=company.shareholder.all())
    context = {
        'form': form,
        'company': company,
        'formset': formset,
    }
    return render(request, 'business_registry/company_edit.html', context)