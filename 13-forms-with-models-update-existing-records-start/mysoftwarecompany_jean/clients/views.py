from django.shortcuts import render, get_object_or_404
from .models import Company, Employee
from .forms import CompanyForm, EmployeeForm

def list_companies(request):
    companies = Company.objects.all()
    return render(request, "clients/companies_list.html", {"companies": companies})

def create_company(request):
    if request.method == "GET":
        form = CompanyForm()
        return render(request, "clients/create_company.html", {"form": form})

    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            new_company = form.save()
            return render(
                request,
                "clients/create_company.html",
                {
                    "form": CompanyForm(),
                    "success": True,
                    "company": new_company
                }
            )
        else:
            return render(request, "clients/create_company.html", {"form": form})

def update_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if request.method == "GET":
        form = CompanyForm(instance=company)
        return render(
            request,
            "clients/update_company.html",
            {"company": company, "form": form}
        )

    if request.method == "POST":
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            updated_company = form.instance

            return render(
                request,
                "clients/update_company.html",
                {
                    "company": updated_company,
                    "form": CompanyForm(instance=updated_company),
                    "success": True
                }
            )
        else:
            return render(
                request,
                "clients/update_company.html",
                {"company": company, "form": form}
            )
    
def company_detail(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    employees = company.employees.all()

    return render(
        request,
        "clients/company_detail.html",
        {
            "company": company,
            "employees": employees
        }
    )

def add_employee(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if request.method == "GET":
        form = EmployeeForm()
        return render(
            request,
            "clients/add_employee.html",
            {"company": company, "form": form}
        )

    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.company = company
            employee.save()

            return render(
                request,
                "clients/add_employee.html",
                {
                    "company": company,
                    "form": EmployeeForm(),
                    "success": True,
                    "employee": employee
                }
            )
        else:
            return render(
                request,
                "clients/add_employee.html",
                {"company": company, "form": form}
            )