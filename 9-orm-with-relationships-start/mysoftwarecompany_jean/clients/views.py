from django.shortcuts import render
from .models import Company

def list_companies(request):
    companies = Company.objects.all()
    return render(request, 'clients/companies_list.html', {'companies': companies})