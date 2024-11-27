from django.shortcuts import render, get_object_or_404, redirect
from .models import Company, Shareholder
from .forms import CompanyForm, ShareholderForm
from django.forms import formset_factory





def company_create(request, pk=None):
    ShareholderFormSet = formset_factory(
    ShareholderForm)

    if request.method == "POST":
        company_form = CompanyForm(request.POST)
        formset = ShareholderFormSet(request.POST)

        if company_form.is_valid() and formset.is_valid():
            company = company_form.save()
            formset.instance = company
            formset.save()
            return redirect("search")  # Replace with your success URL

    else:
        company_form = CompanyForm()
        formset = ShareholderFormSet()

    return render(
        request,
        "business_registry/company_create.html",
        {
            "form": company_form,
            "contact_form": formset,
        },
    )