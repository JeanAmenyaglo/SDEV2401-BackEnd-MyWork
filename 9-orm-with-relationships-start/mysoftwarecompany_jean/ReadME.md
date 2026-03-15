# 🏗️ **1. Project Structure**

Your project looks like this:

```
mysoftwarecompany_jean/
│
├── clients/
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── templates/
│       └── clients/
│           └── companies_list.html
│
├── templates/
│   └── base.html
│
├── manage.py
└── db.sqlite3
```

### ✔️ Why this structure matters  
Django looks for templates in two places:

- App templates (`clients/templates/clients/...`)
- Project templates (`templates/`)

You used **both**, which is the correct professional setup.

---

# 🧱 **2. Models — The Database Structure**

## **clients/models.py**

```python
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Employee(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="employees"
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
```

### ✔️ Why these fields exist  
- `CharField` → short text  
- `EmailField` → validated email  
- `TextField` → long descriptions  
- `DateTimeField` → timestamps  
- `ForeignKey` → relationship (one company → many employees)  

### ✔️ Why `related_name="employees"`  
It allows:

```python
company.employees.all()
```

This is used directly in your template.

---

# 🔄 **3. Migrations**

Commands:

```
python manage.py makemigrations
python manage.py migrate
```

### ✔️ Why migrations matter  
They convert your Python model code into actual database tables.

---

# 🛠️ **4. Admin Setup**

## **clients/admin.py**

```python
from django.contrib import admin
from .models import Company, Employee

admin.site.register(Company)
admin.site.register(Employee)
```

### ✔️ Why this matters  
This gives you a GUI to add companies and employees.

---

# 🌐 **5. Views — Fetching Data**

## **clients/views.py**

```python
from django.shortcuts import render
from .models import Company

def list_companies(request):
    companies = Company.objects.all()
    return render(request, 'clients/companies_list.html', {'companies': companies})
```

### ✔️ Why this view exists  
It:

1. Reads data from the database  
2. Sends it to the template  
3. Renders HTML  

This is the core of Django.

---

# 🧭 **6. URLs — Connecting Views to the Browser**

## **clients/urls.py**

```python
from django.urls import path
from .views import list_companies

urlpatterns = [
    path('companies/', list_companies, name='companies_list'),
]
```

## **project-level urls.py**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('clients.urls')),
]
```

### ✔️ Why this matters  
This makes the page available at:

```
http://127.0.0.1:8000/companies/
```

---

# 🎨 **7. Templates — Displaying Data**

## **templates/base.html**

This is your layout wrapper.  
All pages extend it.

---

## **clients/templates/clients/companies_list.html**

```html
{% extends "base.html" %}

{% block content %}
<div class="container mt-4">
    <h1>Companies list</h1>

    {% for company in companies %}
        <li class="mb-4 p-3 border rounded">
            <strong>{{ company.name }}</strong>
            <div>Email: {{ company.email }}</div>
            <p>{{ company.description }}</p>

            <p>Created at: {{ company.created_at }}</p>
            <p>Information Last updated: {{ company.updated_at }}</p>

            <h4>Employees:</h4>
            <ul>
                {% for employee in company.employees.all %}
                    <li>{{ employee.first_name }} {{ employee.last_name }} — {{ employee.position }}</li>
                {% empty %}
                    <li>No employees yet.</li>
                {% endfor %}
            </ul>
        </li>
    {% endfor %}
</div>
{% endblock %}
```

### ✔️ Why this template is important  
It demonstrates:

- Template inheritance  
- ORM data rendering  
- Reverse relationships  
- Loops  
- Conditional rendering  

This is real‑world Django.

---

# 🔗 **8. How Everything Connects (Beginner‑Friendly)**

Here is the full flow:

```
Browser → URL → View → ORM → Template → HTML → Browser
```

Or in your project:

```
/companies/ → clients/urls.py → list_companies() → Company.objects.all() → companies_list.html → rendered page
```

This is the Django request cycle.

---

# 🏁 **Conclusion**

You built a complete Django mini‑application that demonstrates:

- Models  
- Relationships  
- ORM queries  
- Template inheritance  
- Admin integration  
- URL routing  
- Data rendering  

This is the foundation of every Django backend system.

