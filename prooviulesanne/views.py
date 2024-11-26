from django.shortcuts import render


def home(request):
    return render(request, 'business_registry/home.html')

def search(request):
    search_info = request.GET.get("search", "")
    print("KATSE", search_info)
    context = {
        "search_info": search_info,
    }
    return render(request, 'business_registry/company_search.html', context)