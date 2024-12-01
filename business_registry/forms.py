
import re
from django import forms
from .models import Company, Shareholder
from django.utils.timezone import now
from django.core.validators import MaxLengthValidator, MinLengthValidator

class CompanyCreationForm(forms.ModelForm):
    established_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date",
                                                                     "class": "form-control",}),
                                                              help_text="Date for the establishment of the company."
                                                              )
    code = forms.CharField(
                            widget=forms.NumberInput(attrs={"type": "number",
                                                           "class": "form-control",
                                                           "maxlength": "7"}),
                            validators=[MaxLengthValidator(7,
                            message="The registration code must not exceed 7 numbers. You entered %(show_value)s number.")],
                            help_text="The registration code must be exactly 7 numbers."
                              )
    name = forms.CharField(
                            widget=forms.TextInput(attrs={"type": "text", "class": "form-control"}),
                            validators=[
                                MaxLengthValidator(100, message="The name must not exceed 100 characters. You entered %(show_value)s character."),
                                MinLengthValidator(3, message="The name must contain at least 3 characters. You entered %(show_value)s character.")
                            ],
                            help_text="The name must contain at least 3 characters and not exceed 100 characters."
                        )
    class Meta:
        model = Company
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if not name == "established_date" or not name == "code" or not name == "name":
                field.widget.attrs["class"] = "form-control"
            
    def clean_code(self):
        code = self.cleaned_data.get('code')
        print("codeY",code)
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
    
    def clean_total_capital(self):
        total_capital = self.cleaned_data.get("total_capital")
        if not total_capital >= 2500:
            raise forms.ValidationError("The total capital must be at least 2500 €.")
        return total_capital
        
class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, min_length=1, help_text="Search by name or registry code.")
    
    def clean_search(self):
        search = self.cleaned_data['search']
        if search.isdigit():
            if len(search) != 7:
                raise forms.ValidationError(f"Registry code must be 7 digits. You have entered {len(search)} digits.")
        return search
    
class ShareholderEditForm(forms.ModelForm):
    share_amount = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}))

    class Meta:
        model = Shareholder
        fields = [ "share_amount"]
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['company'].widget.attrs['readonly'] = True
    #     self.fields['company'].widget.attrs['disabled'] = True