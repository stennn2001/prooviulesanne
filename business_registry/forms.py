from django import forms
from .models import Company, Shareholder


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'registration_code', 'establishment_date', 'total_capital']


class ShareholderForm(forms.ModelForm):
    class Meta:
        model = Shareholder
        fields = ['name', 'legal_entity', 'share_amount', 'is_founder']

# Create an inline formset for shareholders linked to the company
# ShareholderFormSet = formset_factory(
#     Shareholder
# )