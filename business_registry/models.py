
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class ShareholderType(models.TextChoices):
    PERSON = "person", "Physical Person"
    COMPANY = "company", "Company"

class BusinessEntityType(models.TextChoices):
    OU = "oü", "OÜ"
    AS = "as", "AS"
    FIE = "fie", "FIE"

class Company(models.Model):
    type = models.CharField(max_length=15, choices=BusinessEntityType.choices, null=False, blank=True)
    name = models.CharField(max_length=100, unique=True)
    total_capital = models.PositiveIntegerField(null=False, blank=False)
    code = models.CharField(max_length=7, unique=True)
    established_date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Companies"
        
    def __str__(self):
        return self.name

class Person(models.Model):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    code = models.IntegerField(unique=True, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Shareholder(models.Model):
    company_id = models.ForeignKey(Company, related_name="shareholder", on_delete=models.CASCADE)
    shareholder_type = models.CharField(max_length=15, choices=ShareholderType.choices)
    shareholder_company_id = models.ForeignKey(Company, related_name="company", on_delete=models.CASCADE, null=True, blank=True)
    shareholder_person_id = models.ForeignKey(Person, related_name="person", on_delete=models.CASCADE, null=True, blank=True)
    is_founder = models.BooleanField(default=False)
    share_amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.shareholder_type == "person":
            return f"Person:{self.shareholder_person_id.first_name} {self.shareholder_person_id.last_name} - {self.company_id.name}"
        elif self.shareholder_type == "company":
            return f"Company:{self.shareholder_company_id.name} - {self.company_id.name}"
        return "N/A"

    def clean(self):
        if self.shareholder_type == "person" and not self.shareholder_person_id:
            raise ValidationError("For shareholder type 'Physical Person', 'Shareholder Person ID' must be filled.")
        if self.shareholder_type == "person" and self.shareholder_company_id:
            raise ValidationError("For shareholder type 'Physical Person', 'Shareholder Company ID' must be empty.")
        if self.shareholder_type == "company" and not self.shareholder_company_id:
            raise ValidationError("For shareholder type 'Company', 'Shareholder Company ID' must be filled.")
        if self.shareholder_type == "company" and self.shareholder_person_id:
            raise ValidationError("For shareholder type 'Company', 'Shareholder Person ID' must be empty.")
