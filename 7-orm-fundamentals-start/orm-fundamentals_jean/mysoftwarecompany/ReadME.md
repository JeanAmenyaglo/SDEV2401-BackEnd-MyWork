# 📘 ORM Fundamentals Lab — Django Models, Migrations & Admin

This lab introduces the core building blocks of Django’s database layer: **models**, **migrations**, the **ORM**, and the **admin interface**.  
By the end of this lab, you will understand how Django stores data, how to create tables, and how to interact with your database using Python instead of SQL.

---

# 🧠 What is the Django ORM?

**ORM** stands for **Object‑Relational Mapper**.

It is Django’s system for converting **Python classes** into **database tables**, and **Python objects** into **database rows**.

Instead of writing SQL like:

```
SELECT * FROM clients_company;
```

You write Python:

```python
Company.objects.all()
```

The ORM handles all the SQL behind the scenes.  
This makes your code:

- easier to read  
- safer  
- database‑independent  
- beginner‑friendly  

The ORM is one of Django’s biggest strengths.

---

# 🚀 What You Built in This Lab

### ✔ A Django project: `mysoftwarecompany`  
### ✔ An app: `clients`  
### ✔ A `Company` model with fields:
- `name`
- `email`
- `phone`

### ✔ An `Employee` model with a ForeignKey to `Company`  
### ✔ Migrations to create database tables  
### ✔ Admin pages to add and manage data  
### ✔ ORM queries to create, read, update, and filter records  

---

# 🏗 Project Setup

### 1. Create and activate a virtual environment

```
python -m venv venv
venv\Scripts\activate
```

### 2. Install Django

```
pip install django
```

### 3. Create the project

```
django-admin startproject mysoftwarecompany .
```

### 4. Create the app

```
python manage.py startapp clients
```

### 5. Add the app to `INSTALLED_APPS`

```python
'clients',
```

---

# 🧩 Creating the Models

## `Company` model

```python
class Company(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=12, null=True)

    def __str__(self):
        return self.name
```

## `Employee` model

```python
class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    position = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
```

---

# 🧱 Migrations (Creating the Database Tables)

Whenever you change a model, run:

```
python manage.py makemigrations
python manage.py migrate
```

This generates SQL and applies it to your database.

---

# 🛠 Adding Models to the Admin

In `clients/admin.py`:

```python
from django.contrib import admin
from .models import Company, Employee

admin.site.register(Company)
admin.site.register(Employee)
```

Create a superuser:

```
python manage.py createsuperuser
```

Then log in at:

```
http://localhost:8000/admin/
```

---

# 🧑‍💼 Adding Data Through the Admin

We added companies and employees through the **admin interface** because:

### ✔ It’s beginner‑friendly  
You get a clean form to fill out — no code required.

### ✔ It shows how Django auto‑generates admin pages  
This is one of Django’s biggest advantages.

### ✔ It helps visualize your data  
You can see rows, edit them, delete them, and confirm everything is working.

### ✔ It mirrors real‑world workflows  
Non‑technical staff often manage data through the admin.

---

# 🐍 Adding Data Through the Django Shell

We also added and updated some data using the **Django shell** because:

### ✔ It teaches you how to use the ORM directly  
This is essential for backend development.

### ✔ It mirrors how your code will interact with the database  
Your views, APIs, and business logic will use the ORM — not the admin.

### ✔ It helps you practice CRUD operations  
Create, Read, Update, Delete — all through Python.

### ✔ It shows how to write database queries without SQL  
This is the core purpose of the ORM.

---

# 🔍 ORM Examples Used in This Lab

### Get all companies

```python
Company.objects.all()
```

### Filter companies

```python
Company.objects.filter(name="Acme Group of Canada")
```

### Get a single company

```python
Company.objects.get(email="cat.sitting@test.com")
```

### Create a new company

```python
Company.objects.create(
    name="Dog Walking Co.",
    email="dog.walking@testing.com",
    phone="7805559999"
)
```

### Update a company

```python
acme = Company.objects.get(name="Acme Group of Canada")
acme.phone = "7801112222"
acme.save()
```

### Get employees for a company

```python
acme.employee_set.all()
```

---

# 🎉 Lab Completed

You now understand:

- How Django models map to database tables  
- How migrations create and update tables  
- How to use the Django admin  
- How to use the ORM to interact with your data  
- How relationships (ForeignKey) work in Django  

This is the foundation of all backend development in Django.
