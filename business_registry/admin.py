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
        from django.contrib.auth.hashers import make_password
        print("Password:", make_password('admin'))
        if obj.shareholder_type == "person" and obj.shareholder_person_id:
            person_name = f"{obj.shareholder_person_id.first_name} {obj.shareholder_person_id.last_name}"
            return format_html(
            '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-rolodex" viewBox="0 0 16 16">'
            '<path d="M8 9.05a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5"/>'
            '<path d="M1 1a1 1 0 0 0-1 1v11a1 1 0 0 0 1 1h.5a.5.5 0 0 0 .5-.5.5.5 0 0 1 1 0 .5.5 0 0 0 .5.5h9a.5.5 0 0 0 .5-.5.5.5 0 0 1 1 0 .5.5 0 0 0 .5.5h.5a1 1 0 0 0 1-1V3a1 1 0 0 0-1-1H6.707L6 1.293A1 1 0 0 0 5.293 1zm0 1h4.293L6 2.707A1 1 0 0 0 6.707 3H15v10h-.085a1.5 1.5 0 0 0-2.4-.63C11.885 11.223 10.554 10 8 10c-2.555 0-3.886 1.224-4.514 2.37a1.5 1.5 0 0 0-2.4.63H1z"/>'
            '</svg> {0}', person_name
        )
        elif obj.shareholder_type == "company" and obj.shareholder_company_id:
            company_name = obj.shareholder_company_id.name
            return format_html(
                '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-buildings-fill" viewBox="0 0 16 16">'
                '<path d="M15 .5a.5.5 0 0 0-.724-.447l-8 4A.5.5 0 0 0 6 4.5v3.14L.342 9.526A.5.5 0 0 0 0 10v5.5a.5.5 0 0 0 .5.5h9a.5.5 0 0 0 .5-.5V14h1v1.5a.5.5 0 0 0 .5.5h3a.5.5 0 0 0 .5-.5zM2 11h1v1H2zm2 0h1v1H4zm-1 2v1H2v-1zm1 0h1v1H4zm9-10v1h-1V3zM8 5h1v1H8zm1 2v1H8V7zM8 9h1v1H8zm2 0h1v1h-1zm-1 2v1H8v-1zm1 0h1v1h-1zm3-2v1h-1V9zm-1 2h1v1h-1zm-2-4h1v1h-1zm3 0v1h-1V7zm-2-2v1h-1V5zm1 0h1v1h-1z"/>'
                '</svg> {0}', company_name
            )
        return "N/A"