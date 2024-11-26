from django import forms
from django.utils.timezone import now
from .models import Company, Shareholder, Person, LegalEntity


class CompanyCreationForm(forms.ModelForm):
    """Form for creating a new company."""

    class Meta:
        model = Company
        fields = [
            'name', 'registration_code', 'establishment_date', 'total_capital'
        ]
        widgets = {
            'establishment_date': forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Loop through each field and apply form-control class
        for _, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_establishment_date(self):
        establishment_date = self.cleaned_data['establishment_date']
        if establishment_date > now().date():
            raise forms.ValidationError(
                "Establishment date cannot be in the future.")
        return establishment_date

    def clean_total_capital(self):
        total_capital = self.cleaned_data['total_capital']
        if total_capital < 2500:
            raise forms.ValidationError(
                "Total capital must be at least €2500.")
        return total_capital

class ShareholderForm(forms.ModelForm):
    class Meta:
        model = Shareholder
        fields = ['person', 'share_amount']
    
    person = forms.ModelChoiceField(queryset=Person.objects.all(), required=False, label="Physical Person", widget=forms.Select(attrs={'class': 'form-control'}))