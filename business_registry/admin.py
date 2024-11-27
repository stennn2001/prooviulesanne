from django.contrib import admin
from .models import Person, LegalEntity, Shareholder, Company

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name",)
    search_fields = ("first_name", "last_name",)


@admin.register(LegalEntity)
class LegalEntityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Shareholder)
class ShareholderAdmin(admin.ModelAdmin):
    list_display = ("legal_entity", "share_amount", "is_founder")
    search_fields = ("person__first_name", "person__last_name", "legal_entity__name")


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "registration_code", "establishment_date", "total_capital")
    search_fields = ("name", "registration_code")
    filter_horizontal = ("shareholders",)