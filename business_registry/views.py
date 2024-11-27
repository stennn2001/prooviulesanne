from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from .models import OsaUhing, Osanik
from .forms import OsaUhingForm, OsanikForm


def company_create(request):
    OsanikFormSet = modelformset_factory(Osanik, form=OsanikForm, extra=1, can_delete=True)

    if request.method == 'POST':
        osa_uhing_form = OsaUhingForm(request.POST)
        osanik_formset = OsanikFormSet(request.POST, queryset=Osanik.objects.none())

        if osa_uhing_form.is_valid() and osanik_formset.is_valid():
            osa_uhing = osa_uhing_form.save()

            for osanik_form in osanik_formset:
                if osanik_form.cleaned_data and not osanik_form.cleaned_data.get('DELETE'):
                    osanik = osanik_form.save(commit=False)
                    osanik.osa_uhing = osa_uhing
                    osanik.save()

            return redirect('company_create')  # Replace with your URL

    else:
        osa_uhing_form = OsaUhingForm()
        osanik_formset = OsanikFormSet(queryset=Osanik.objects.none())

    return render(request, 'business_registry/company_create.html', {
        'osa_uhing_form': osa_uhing_form,
        'osanik_formset': osanik_formset,
    })