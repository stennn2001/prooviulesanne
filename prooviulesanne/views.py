from django.shortcuts import render


def home(request):
    return render(request, 'business_registry/home.html')



