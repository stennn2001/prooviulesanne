from django.contrib import admin
from .models import Company, Person, Shareholder
from django.utils.html import format_html


class ShareholderInline(admin.TabularInline):
    model = Shareholder
    fk_name = "company_id"
    extra = 1

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "code", "type", "established_date", "total_capital", "owned_capital", "owners"]
    search_fields = ["name", "code"]
    inlines = [ShareholderInline]

    def owned_capital(self, obj):
        return sum(share.share_amount for share in obj.shareholder.all())
    
    def owners(self, obj):
        shareholders = obj.shareholder.all()
        owners_list = []
        for shareholder in shareholders:
            if shareholder.shareholder_type == "person":
                person = shareholder.shareholder_person_id
                if person:
                    owners_list.append(f"{person.first_name} {person.last_name}")
            elif shareholder.shareholder_type == "company":
                company = shareholder.shareholder_company_id
                if company:
                    owners_list.append(company.name)
        return ", ".join(owners_list)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "code"]
    search_fields = ["first_name", "last_name", "code"]


@admin.register(Shareholder)
class ShareholderAdmin(admin.ModelAdmin):
    list_display = ["company_id", "get_shareholder", "shareholder_type", "is_founder", "share_amount"]
    search_fields = ["company_id__name", "shareholder_person_id__first_name", "shareholder_person_id__last_name", "shareholder_company_id__name"]

    def get_shareholder(self, obj):
        if obj.shareholder_type == "person" and obj.shareholder_person_id:
            person_name = f"{obj.shareholder_person_id.first_name} {obj.shareholder_person_id.last_name}"
            return format_html(f'<i class="bi bi-person text-primary pe-1"></i>{person_name}')
        elif obj.shareholder_type == "company" and obj.shareholder_company_id:
            company_name = obj.shareholder_company_id.name
            return format_html(f'<i class="bi bi-building text-primary pe-1"></i>{company_name}')
        return "N/A"