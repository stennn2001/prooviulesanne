
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class ShareholderType(models.TextChoices):
    PERSON = "person", "Physical Person"
    COMPANY = "company", "Company"

class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    registration_code = models.CharField(max_length=7, unique=True)
    established_date = models.DateField()
    total_capital = models.PositiveIntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Shareholder(models.Model):
    type = models.CharField(max_length=15, choices=ShareholderType.choices)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    identification_code = models.IntegerField(unique=True, null=True, blank=True)
    entity_name = models.CharField(max_length=100, null=True, blank=True)
    entity_reg_code = models.CharField(max_length=7, unique=True, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.type == "person":
            return f"Person: {self.first_name} {self.last_name}"
        return f"Company: {self.entity_name} ({self.entity_reg_code})"

class CompanyShareholder(models.Model):
    company = models.ForeignKey(Company, related_name="shareholder", on_delete=models.CASCADE)
    shareholder = models.ForeignKey(Shareholder, related_name="companies", on_delete=models.CASCADE)
    ownership_share = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    is_founder = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.shareholder} - {self.company}"
