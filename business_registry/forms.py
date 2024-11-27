from django import forms
from django.utils.timezone import now
from .models import Company

class CompanyCreationForm(forms.ModelForm):
    model = Company
    fields = "__all__"