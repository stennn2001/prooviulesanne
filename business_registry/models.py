from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now


def validate_kogukapital(value):
    if value < 2500:
        raise ValidationError("Kogukapitali suurus peab olema vähemalt 2500 eurot.")


def validate_nimi(value):
    if len(value) < 3 or len(value) > 100:
        raise ValidationError("Nimi peab olema 3 kuni 100 tähemärki pikk.")


class OsaUhing(models.Model):
    nimi = models.CharField(
        max_length=100,
        unique=True,
        validators=[validate_nimi],
        help_text="Sisesta nimi, 3 kuni 100 tähte või numbrit."
    )
    registrikood = models.CharField(
        max_length=7,
        unique=True,
        help_text="Registrikood peab olema täpselt 7 numbrit."
    )
    asutamiskuupaev = models.DateField(
        help_text="Asutamiskuupäev peab olema väiksem või võrdne tänase kuupäevaga."
    )
    kogukapital = models.PositiveIntegerField(
        validators=[validate_kogukapital],
        help_text="Kogukapitali suurus peab olema vähemalt 2500 eurot."
    )

    def __str__(self):
        return self.nimi


class Osanik(models.Model):
    osa_uhing = models.ForeignKey(OsaUhing, related_name='osanikud', on_delete=models.CASCADE)
    nimi = models.CharField(max_length=100, help_text="Osaniku nimi.")
    osa_suurus = models.PositiveIntegerField(
        help_text="Osaniku osa suurus eurodes (vähemalt 1)."
    )

    def __str__(self):
        return f"{self.nimi} ({self.osa_suurus}€)"