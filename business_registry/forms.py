
from django import forms
from .models import Company, CompanyShareholder
from django.utils.timezone import now

class CompanyCreationForm(forms.ModelForm):
    established_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    class Meta:
        model = Company
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name == "established_date":
                field.widget.attrs["dateFormat"] = "dd/mm/yy"
            field.widget.attrs["class"] = "form-control"
            
    def clean_registration_code(self):
        registration_code = self.cleaned_data['registration_code']
        if not registration_code.isdigit():
            raise forms.ValidationError("The registration code must contain only digits.")
        return registration_code
    
    def clean_established_date(self):
        established_date = self.cleaned_data.get("established_date")
        current_date = now().date()
        if established_date > current_date:
            raise forms.ValidationError("The establishment date cannot be in the future.")
        return established_date
        
class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, min_length=1, help_text="Search by name or registry code.")
    
    def clean_search(self):
        search = self.cleaned_data['search']
        if search.isdigit():
            if len(search) != 7:
                raise forms.ValidationError(f"Registry code must be 7 digits. You have entered {len(search)} digits.")
        return search
    
class CompanyShareholderEditForm(forms.ModelForm):
    #company = forms.ModelChoiceField(queryset=Company.objects.filter(), widget=forms.Select(attrs={'class': 'form-control'}))
    shareholder = forms.ModelChoiceField(queryset=CompanyShareholder.objects.all(), label="", widget=forms.Select(attrs={'class': 'form-control',
                                                                                                               #'disabled': True
                                                                                                               }))
    class Meta:
        model = CompanyShareholder
        fields = ["shareholder", "ownership_share"]
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['company'].widget.attrs['readonly'] = True
    #     self.fields['company'].widget.attrs['disabled'] = True