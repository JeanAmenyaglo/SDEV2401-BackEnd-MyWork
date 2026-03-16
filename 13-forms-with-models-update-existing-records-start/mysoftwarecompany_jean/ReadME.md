
# 📘 **Django Lab: Companies & Employees Management**  
A complete Django application that allows users to:

- Create companies  
- Update companies  
- View company details  
- Add employees to a company  
- Display employees on the company detail page  

This README walks through the entire lab from start to finish.

---

# 🚀 **1. Project Setup**

### **Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### **Install Django**
```bash
pip install django
```

### **Create the Django project**
```bash
django-admin startproject mysoftwarecompany
cd mysoftwarecompany
```

### **Create the app**
```bash
python manage.py startapp clients
```

### **Add the app to settings**
In `mysoftwarecompany/settings.py`:

```python
INSTALLED_APPS = [
    ...
    'clients',
]
```

---

# 🗂️ **2. Project Structure**

Your final structure should look like:

```
mysoftwarecompany/
    mysoftwarecompany/
    clients/
        templates/
            clients/
                base.html
                companies_list.html
                create_company.html
                update_company.html
                company_detail.html
                add_employee.html
        models.py
        forms.py
        views.py
        urls.py
    manage.py
```

---

# 🧱 **3. Models**

In `clients/models.py`:

```python
class Company(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Employee(models.Model):
    company = models.ForeignKey(Company, related_name="employees", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# 📝 **4. Forms**

In `clients/forms.py`:

```python
from django import forms
from .models import Company, Employee

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'email', 'description']


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'role']
```

---

# 🌐 **5. URLs**

### **Project-level URLs** (`mysoftwarecompany/urls.py`)
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('clients/', include('clients.urls')),
]
```

### **App-level URLs** (`clients/urls.py`)
```python
urlpatterns = [
    path('', views.list_companies, name='list_companies'),
    path('company/create/', views.create_company, name='create_company'),
    path('company/<int:company_id>/', views.company_detail, name='company_detail'),
    path('company/<int:company_id>/update/', views.update_company, name='update_company'),
    path('company/<int:company_id>/employee/add/', views.add_employee, name='add_employee'),
]
```

---

# 🧠 **6. Views**

### **List Companies**
```python
def list_companies(request):
    companies = Company.objects.all()
    return render(request, "clients/companies_list.html", {"companies": companies})
```

### **Create Company**
```python
def create_company(request):
    if request.method == "GET":
        form = CompanyForm()
        return render(request, "clients/create_company.html", {"form": form})

    form = CompanyForm(request.POST)
    if form.is_valid():
        form.save()
        return render(request, "clients/create_company.html", {"form": CompanyForm(), "success": True})

    return render(request, "clients/create_company.html", {"form": form})
```

### **Update Company**
```python
def update_company(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if request.method == "GET":
        form = CompanyForm(instance=company)
        return render(request, "clients/update_company.html", {"company": company, "form": form})

    form = CompanyForm(request.POST, instance=company)
    if form.is_valid():
        form.save()
        return render(request, "clients/update_company.html", {"company": company, "form": form, "success": True})

    return render(request, "clients/update_company.html", {"company": company, "form": form})
```

### **Company Detail**
```python
def company_detail(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    employees = company.employees.all()
    return render(request, "clients/company_detail.html", {"company": company, "employees": employees})
```

### **Add Employee**
```python
def add_employee(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    if request.method == "GET":
        form = EmployeeForm()
        return render(request, "clients/add_employee.html", {"company": company, "form": form})

    form = EmployeeForm(request.POST)
    if form.is_valid():
        employee = form.save(commit=False)
        employee.company = company
        employee.save()
        return render(request, "clients/add_employee.html", {"company": company, "form": EmployeeForm(), "success": True})

    return render(request, "clients/add_employee.html", {"company": company, "form": form})
```

---

# 🎨 **7. Templates**

### **Base Template**
```html
<!DOCTYPE html>
<html>
<head>
    <title>My Software Company</title>
</head>
<body>
    <nav style="margin-bottom: 20px;">
        <a href="{% url 'list_companies' %}">Home</a> |
        <a href="{% url 'create_company' %}">Create Company</a>
    </nav>

    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

(Other templates follow the same structure.)

---

# 🧪 **8. Testing the Application**

### **Start the server**
```bash
python manage.py runserver
```

### **Test each feature**
1. **List companies**  
   `http://127.0.0.1:8000/clients/`

2. **Create company**  
   `http://127.0.0.1:8000/clients/company/create/`

3. **View company detail**  
   `http://127.0.0.1:8000/clients/company/<ID>/`

4. **Update company**  
   `http://127.0.0.1:8000/clients/company/<ID>/update/`

5. **Add employee**  
   `http://127.0.0.1:8000/clients/company/<ID>/employee/add/`

6. **Verify employees appear on the detail page**

---

# 🎉 **Lab Completed**

