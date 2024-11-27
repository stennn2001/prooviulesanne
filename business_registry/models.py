from django.db import models
from django.core.validators import MinValueValidator

class StakeholderType(models.TextChoices):
    PERSON = 'person', 'Physical Person'
    ENTITY = 'entity', 'Legal Entity'

class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    registration_code = models.CharField(max_length=7, unique=True)
    established_date = models.DateField()
    total_capital = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Stakeholder(models.Model):
    type = models.CharField(max_length=6, choices=StakeholderType.choices)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    identification_code = models.IntegerField(max_length=11, min_length=11, unique=True, null=True, blank=True)
    entity_name = models.CharField(max_length=100, null=True, blank=True)
    entity_reg_code = models.CharField(max_length=7, unique=True, null=True, blank=True)

    def __str__(self):
        if self.type == 'person':
            return f'Person: {self.first_name} {self.last_name}'
        return f"Legal Enityt: {self.entity_name} ({self.entity_reg_code})"

class CompanyStakeholder(models.Model):
    company = models.ForeignKey(Company, related_name='stakeholders', on_delete=models.CASCADE)
    stakeholder = models.ForeignKey(Stakeholder, related_name='companies', on_delete=models.CASCADE)
    ownership_share = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    is_founder = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.stakeholder} - {self.company}'