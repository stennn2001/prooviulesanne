from django.contrib import admin
from .models import Company, Shareholder, CompanyShareholder


class CompanyInline(admin.TabularInline):
    model = CompanyShareholder
    extra = 1

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "registration_code", "established_date", "total_capital", "owned_capital", "owners"]
    search_fields = ["name", "registration_code"]
    inlines = [CompanyInline]

    def owned_capital(self, obj):
        return sum([shareholder.ownership_share for shareholder in obj.shareholder.all()])
    
    def owners(self, obj):
        shareholders = obj.shareholder.all() 
        owners = []
        for share in shareholders:
            owners.append(share)
        return ", ".join([str(owner) for owner in owners])

@admin.register(Shareholder)
class ShareholderAdmin(admin.ModelAdmin):
    list_display = ["get_name", "type", "identification_code", "entity_reg_code"]
    search_fields = ["first_name", "last_name", "personal_code", "entity_name"]

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}" if obj.type == "person" else obj.entity_name

@admin.register(CompanyShareholder)
class CompanyShareholderAdmin(admin.ModelAdmin):
    list_display = ["company", "shareholder", "ownership_share", "is_founder"]
    search_fields = ["company__name", "shareholder__first_name", "shareholder__last_name", "shareholder__entity_name"]