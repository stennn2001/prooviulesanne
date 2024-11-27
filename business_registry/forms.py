from django import forms
from django.core.exceptions import ValidationError
from .models import OsaUhing, Osanik


class OsaUhingForm(forms.ModelForm):
    class Meta:
        model = OsaUhing
        fields = ['nimi', 'registrikood', 'asutamiskuupaev', 'kogukapital']

    def clean_asutamiskuupaev(self):
        asutamiskuupaev = self.cleaned_data.get('asutamiskuupaev')
        if asutamiskuupaev > now().date():
            raise ValidationError("Asutamiskuupäev ei tohi olla tulevikus.")
        return asutamiskuupaev


class OsanikForm(forms.ModelForm):
    class Meta:
        model = Osanik
        fields = ['nimi', 'osa_suurus']