
from django import forms
from .models import Company, Shareholder
from django.utils.timezone import now
from django.core.validators import MaxLengthValidator

class CompanyCreationForm(forms.ModelForm):
    established_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    code = forms.CharField(widget=forms.NumberInput(attrs={"type": "number","maxlength": "7"}),
                              validators=[MaxLengthValidator(7,
                                message="The registration code must not exceed 7 numbers. You entered %(show_value)s number.")])
    class Meta:
        model = Company
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for _, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            
    def clean_code(self):
        code = self.cleaned_data['code']
        if not code.isdigit():
            raise forms.ValidationError("The registration code must contain only digits.")
        elif len(code) != 7:
            raise forms.ValidationError(f"The registration code must be 7 digits. You have entered {len(code)} digit{'s' if len(code) != 1 else ''}.")
        return code
    
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
    
class ShareholderEditForm(forms.ModelForm):
    #company = forms.ModelChoiceField(queryset=Company.objects.filter(), widget=forms.Select(attrs={'class': 'form-control'}))
    shareholder = forms.ModelChoiceField(queryset=Shareholder.objects.all(), label="", widget=forms.Select(attrs={'class': 'form-control',
                                                                                                               #'disabled': True
                                                                                                               }))
    class Meta:
        model = Shareholder
        fields = ["shareholder", "share_amount"]
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['company'].widget.attrs['readonly'] = True
    #     self.fields['company'].widget.attrs['disabled'] = True