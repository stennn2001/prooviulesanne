from django.contrib import admin
from .models import OsaUhing, Osanik

@admin.register(OsaUhing)
class OsaUhingAdmin(admin.ModelAdmin):
    list_display = ['nimi', 'registrikood', 'asutamiskuupaev', 'kogukapital']


@admin.register(Osanik)
class OsanikAdmin(admin.ModelAdmin):
    list_display = ['nimi', 'osa_uhing', 'osa_suurus']