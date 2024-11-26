from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.utils.timezone import now
from django.core.exceptions import ValidationError



class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class LegalEntity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.registration_code})"


class Shareholder(models.Model):
    name = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True)
    legal_entity = models.ForeignKey(LegalEntity, on_delete=models.CASCADE, null=True, blank=True)
    share_amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    is_founder = models.BooleanField(default=False)

    def __str__(self):
        if self.person:
            return f"Shareholder: {self.person}"
        return f"Shareholder: {self.legal_entity}"


class Company(models.Model):
    name = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    registration_code = models.IntegerField(unique=True, validators=[MaxValueValidator(7)])
    establishment_date = models.DateField(validators=[MaxValueValidator(limit_value=now().date())])
    total_capital = models.PositiveIntegerField(validators=[MinValueValidator(2500)])
    shareholders = models.ManyToManyField(Shareholder, related_name="companies")

    def __str__(self):
        return f"{self.name} ({self.registration_code})"

    def clean(self):
        super().clean()
        if self.shareholders.exists():
            total_shares = sum(share.share_amount for share in self.shareholders.all())
            if total_shares != self.total_capital:
                raise ValidationError("Sum of shareholder shares must equal total capital.")
            
    def clean_validate_registration_code(self, value):
        if len(str(value)) != 7:
            raise ValidationError("The registration code must be exactly 7 digits.")
        if not str(value).isdigit():
            raise ValidationError("The registration code must contain only digits.")