from django.shortcuts import render
from .forms import CompanyCreationForm

# Create your views here.
def company_create(request):
    
    if request.method == "POST":
        form = CompanyCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print("KATSE", form.cleaned_data)
    else:
        form = CompanyCreationForm()
    context= {
        "form": form
    }
    return render(request, "business_registry/company_create.html", context)