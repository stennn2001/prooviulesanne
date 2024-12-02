from django.shortcuts import render
from .models import Company, Shareholder, Person
from django.http import JsonResponse
from django.db.models import Q
from .forms import CompanyCreationForm, SearchForm, ShareholderEditForm
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
import json

# Create your views here.


def format_price(value):

    return f"{value:,}".replace(",", " ") + " €"


def has_array_items(obj):
    return isinstance(obj, list) and len(obj) > 0


def company_create(request):
    shareholders_json_errors = []

    if request.method == "POST":
        shareholders_json_value = request.POST.get("shareholders_json",
                                                   '').strip()

        try:
            shareholders = json.loads(shareholders_json_value)
        except json.JSONDecodeError:
            shareholders = []

        if not has_array_items(shareholders):
            shareholders_json_errors.append("Shareholders cannot be empty.")

        form = CompanyCreationForm(request.POST)

        total_share_amount = 0
        company_total_capital = request.POST.get("total_capital", None).strip()
        for shareholder in shareholders:
            share_amount = shareholder.get("share_amount", None)
            if share_amount is None or share_amount < 1:
                shareholders_json_errors.append(
                    f"Shareholder \"{shareholder['name']}\" share amount must be at least 1."
                )
            if share_amount is not None:
                total_share_amount += int(share_amount)

        if total_share_amount and company_total_capital.isdigit() and int(
                total_share_amount) != int(company_total_capital):
            shareholders_json_errors.append(
                f'''Total share amount ({format_price(int(total_share_amount))})
                must be equal to the total capital ({format_price(int(company_total_capital))}).'''
            )

        if form.is_valid() and not shareholders_json_errors:
            new_company = form.save()
            for shareholder in shareholders:
                if shareholder['type'].lower() == 'person':
                    person = Person.objects.filter(
                        id=shareholder['id']).first()
                    if person:
                        Shareholder.objects.create(
                            company_id=new_company,
                            shareholder_type="person",
                            shareholder_person_id=person,
                            is_founder=True,
                            share_amount=shareholder['share_amount'],
                        )
                elif shareholder['type'].lower() == 'company':
                    company = Company.objects.filter(
                        id=shareholder['id']).first()
                    if company:
                        Shareholder.objects.create(
                            company_id=new_company,
                            shareholder_type="company",
                            shareholder_company_id=company,
                            is_founder=True,
                            share_amount=shareholder['share_amount'],
                        )
            messages.success(
                request, f"Company '{new_company.name}' created successfully.")
            return redirect("company_detail", company_id=new_company.id)
        else:
            print(form.errors)
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


def person_detail(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    if person:
        shareholder_company = Shareholder.objects.filter(
            shareholder_person_id=person).all()
    context = {"person": person, "shareholder_company": shareholder_company}
    return render(request, 'business_registry/person_detail.html', context)


def search(request):
    form = SearchForm(request.GET or None)
    search_info = request.GET.get("search", "")

    if form.is_valid():
        search_info = form.cleaned_data.get("search", "")
        companies_search = Company.objects.filter(
            Q(name__icontains=search_info) | Q(code__icontains=search_info))
        person_search = Person.objects.filter(
            Q(first_name__icontains=search_info)
            | Q(last_name__icontains=search_info)
            | Q(code__icontains=search_info))
        combined_search = list(companies_search) + list(person_search)

        total_length_search = len(combined_search)
        if companies_search:
            messages.success(
                request,
                f"Success, found {total_length_search} {'matches' if total_length_search != 1 else 'match'}."
            )
        else:
            messages.info(request, "No search results")
    else:
        combined_search = None

    context = {
        "form": form,
        "search_info": search_info,
        "combined_search": combined_search
    }
    return render(request, 'business_registry/company_search.html', context)


def search_shareholders(request):
    search_phrase = request.GET.get("search", "").strip()

    if search_phrase:
        company_results = Company.objects.filter(
            Q(name__icontains=search_phrase)
            | Q(code__icontains=search_phrase)).values("id", "name", "code")
        person_results = Person.objects.filter(
            Q(first_name__icontains=search_phrase)
            | Q(last_name__icontains=search_phrase)
            | Q(code__icontains=search_phrase)).values("id", "first_name",
                                                       "last_name", "code")

        for company in company_results:
            company["type"] = "company"
        for person in person_results:
            person["type"] = "person"

        shareholders = list(company_results) + list(person_results)
    else:
        shareholders = []

    return JsonResponse({"shareholders": shareholders})


def company_edit(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    shareholders = company.shareholder.all()

    if request.method == 'POST':
        forms = []
        total_share_amount = 0

        post_data = request.POST
        for shareholder in shareholders:
            share_amount_key = f"share_amount_{shareholder.id}"
            share_amount = post_data.get(share_amount_key, "")

            if not share_amount.isdigit():
                messages.error(
                    request,
                    f"Invalid share amount for shareholder {shareholder.name}."
                )
                return redirect("company_edit", company_id=company.id)

            share_amount = int(share_amount)
            total_share_amount += share_amount

            form_data = post_data.copy()
            form_data["share_amount"] = share_amount
            form = ShareholderEditForm(form_data, instance=shareholder)
            forms.append(form)

        if total_share_amount != company.total_capital:
            messages.error(
                request,
                "Total shareholder amount must be equal to company total capital."
            )
            return redirect("company_edit", company_id=company.id)

        for form in forms:
            if form.is_valid():
                form.save()
        messages.success(request, "Shareholders updated successfully.")
        return redirect("company_detail", company_id=company.id)
    else:
        forms = []
        for shareholder in shareholders:
            form = ShareholderEditForm(instance=shareholder)
            forms.append(form)
        lists = zip(forms, shareholders)

    context = {
        "shareholders": shareholders,
        "company": company,
        "forms": forms,
        "lists": lists
    }

    return render(request, 'business_registry/company_edit.html', context)
