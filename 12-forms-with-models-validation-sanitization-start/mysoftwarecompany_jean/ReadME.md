# Lab 12 – Forms with Models, Validation & Sanitization

This README assumes you **copied your working Lab 11 project** into this new lab folder and are now adding the **new requirements for Lab 12** on top of it.

You already had:

- A Django project (`mysoftwarecompany_jean`)
- The `clients` app
- Contact form + Newsletter form
- Base template and basic URL wiring

Lab 12 extends that by adding:

- A `Company` model and `Role` model
- ModelForms (`CompanyForm`, `RoleForm`)
- Field‑level and cross‑field validation
- Non‑field errors in templates
- Success messages and detail links

---

## 1. Starting point

You begin this lab by:

- **Copying the previous lab folder** (Lab 11) into a new directory for Lab 12.
- Ensuring the project runs:

```bash
python manage.py runserver
```

**Why:**  
We reuse the working foundation (settings, base.html, contact/newsletter views, email config) so Lab 12 focuses only on **models + ModelForms + validation**, not redoing setup.

---

## 2. Add models for this lab

### 2.1 Open `clients/models.py`

Replace its contents with:

```python
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
```

**Why:**

- **`Company`** is the main entity for this lab—used with a ModelForm, validated, and displayed on a detail page.
- **`email`** is unique so we can validate against duplicates.
- **`description`** and **`phone_number`** support extra validation challenges.
- **`created_at` / `updated_at`** give audit info and make the detail page feel real.
- **`Role`** is used for the challenge: creating roles with validation.

### 2.2 Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

**Why:**  
Django needs to create/update the database tables to match the new models.

---

## 3. Add ModelForms with validation

### 3.1 Open `clients/forms.py`

Ensure you have the imports:

```python
from django import forms
from .models import Company, Role
```

Add or update the file to include:

```python
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class NewsletterSignupForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
```

Then add the **new** forms:

```python
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name", "email", "website", "description", "phone_number"]

    def clean_name(self):
        name = self.cleaned_data.get("name", "")
        if len(name) < 3:
            raise forms.ValidationError("Company name must be at least 3 characters long.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description", "")
        if len(description) < 30:
            raise forms.ValidationError("Description must be at least 30 characters long.")
        return description

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        name = cleaned_data.get("name", "")
        description = cleaned_data.get("description", "")

        # Unique email
        if email and Company.objects.filter(email=email).exists():
            self.add_error("email", "A company with this email already exists.")

        # Forbidden words
        forbidden_words = ["spam", "fake", "scam"]
        for word in forbidden_words:
            if word in name.lower() or word in description.lower():
                raise forms.ValidationError(
                    f"The company contains a forbidden word: {word}"
                )

        # Phone number validation
        phone = cleaned_data.get("phone_number", "")
        digits = [c for c in phone if c.isdigit()]
        if phone and len(digits) != 10:
            self.add_error("phone_number", "Phone number must contain exactly 10 digits.")

        return cleaned_data


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data.get("name", "")
        if len(name) < 4:
            raise forms.ValidationError("Role name must be at least 4 characters long.")
        return name
```

**Why:**

- **ModelForm** (`CompanyForm`) automatically maps fields to the `Company` model and handles saving.
- `clean_<fieldname>` methods (`clean_name`, `clean_description`) enforce **field-level validation**.
- `clean()` enforces **cross-field and database-based validation**:
  - Unique email
  - Forbidden words in name/description
  - Phone number format
- `RoleForm` demonstrates another ModelForm with simple validation.

---

## 4. Add views that use the ModelForms

### 4.1 Open `clients/views.py`

At the top, ensure imports:

```python
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail

from .forms import (
    ContactForm,
    NewsletterSignupForm,
    CompanyForm,
    RoleForm,
)
from .models import Company, Role
```

Keep your existing `contact_us` and `newsletter` views from Lab 11.

Add the **create_company** view:

```python
def create_company(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            company = form.instance
            return render(
                request,
                "clients/create_company.html",
                {"form": CompanyForm(), "new_company": company},
            )
        return render(request, "clients/create_company.html", {"form": form})

    form = CompanyForm()
    return render(request, "clients/create_company.html", {"form": form})
```

**Why:**

- On **GET**, we show an empty form.
- On **POST**, we validate:
  - If valid → save to DB, show success message + link to detail page.
  - If invalid → re-render form with errors.
- Passing `new_company` to the template allows us to show a success banner and a link.

Add the **company_detail** view:

```python
def company_detail(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    return render(request, "clients/company_detail.html", {"company": company})
```

**Why:**

- `get_object_or_404` fetches the company or returns a 404 if not found.
- This view powers the “View Company Details” link after creation.

Add the **create_role** view (challenge):

```python
def create_role(request):
    if request.method == "POST":
        form = RoleForm(request.POST)
        if form.is_valid():
            role = form.save()
            return render(
                request,
                "clients/create_role.html",
                {"form": RoleForm(), "new_role": role},
            )
        return render(request, "clients/create_role.html", {"form": form})

    form = RoleForm()
    return render(request, "clients/create_role.html", {"form": form})
```

**Why:**

- Mirrors the company creation flow but for `Role`.
- Demonstrates reuse of the same pattern with another model.

---

## 5. Wire URLs

### 5.1 Open `clients/urls.py`

Make sure it looks like:

```python
from django.urls import path
from .views import (
    contact_us,
    newsletter,
    create_company,
    company_detail,
    create_role,
)

urlpatterns = [
    path("contact/", contact_us, name="contact_us"),
    path("newsletter-signup/", newsletter, name="newsletter_signup"),
    path("company/create/", create_company, name="create_company"),
    path("company/<int:company_id>/", company_detail, name="company_detail"),
    path("role/create/", create_role, name="create_role"),
]
```

**Why:**

- `company/create/` → shows the company creation form.
- `company/<int:company_id>/` → shows the detail page for a specific company.
- `role/create/` → shows the role creation form.
- Names (`create_company`, `company_detail`, `create_role`) are used in templates via `{% url %}`.

Your project’s root `urls.py` already includes `clients.urls` from Lab 11, so no change needed there.

---

## 6. Create templates

### 6.1 `create_company.html`

Create:

`clients/templates/clients/create_company.html`

```html
{% extends 'base.html' %}

{% block content %}
<div class="max-w-2xl mx-auto">
    <h1 class="text-3xl font-bold underline">Create a new Company</h1>

    {% if new_company %}
    <div class="mt-4 p-4 bg-green-100 text-green-800 border border-green-200 rounded">
        Company "{{ new_company.name }}" has been created successfully.
        <a href="{% url 'company_detail' new_company.id %}" class="text-blue-600 underline">
            View Company Details
        </a>
    </div>
    {% endif %}

    {% if form.non_field_errors %}
    <div class="mb-4 p-4 bg-red-100 text-red-800 border border-red-200 rounded">
        <ul>
            {% for error in form.non_field_errors %}
            <li>{{ error }}</li>
            {% endfor %}
        </ul>
    </div>
    {% endif %}

    <form method="post" class="mt-4">
        {% csrf_token %}
        {% for field in form %}
        <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700">{{ field.label }}</label>
            {{ field }}
            {% if field.errors %}
            <p class="text-sm text-red-500 mt-1">{{ field.errors|striptags }}</p>
            {% endif %}
        </div>
        {% endfor %}
        <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded">Submit</button>
    </form>
</div>
{% endblock %}
```

**Why:**

- Shows a success banner when `new_company` is present.
- Uses `{% url 'company_detail' new_company.id %}` to link to the detail page.
- Renders **non-field errors** (from `clean()`) above the form.
- Renders **field errors** under each field.

### 6.2 `company_detail.html`

Create:

`clients/templates/clients/company_detail.html`

```html
{% extends 'base.html' %}

{% block content %}
<div class="max-w-2xl mx-auto">
    <h1 class="text-3xl font-bold underline">Company Details</h1>

    <div class="mt-4 p-4 bg-white shadow rounded">
        <p><strong>Name:</strong> {{ company.name }}</p>
        <p><strong>Email:</strong> {{ company.email }}</p>
        <p><strong>Website:</strong> {{ company.website }}</p>
        <p><strong>Description:</strong> {{ company.description }}</p>
        <p><strong>Phone:</strong> {{ company.phone_number }}</p>
        <p class="text-sm text-gray-500 mt-2">
            Created at: {{ company.created_at }} | Updated at: {{ company.updated_at }}
        </p>
    </div>
</div>
{% endblock %}
```

**Why:**

- Displays all key fields of the `Company` instance.
- Uses the timestamps to show that the record is persisted and updated.

### 6.3 `create_role.html`

Create:

`clients/templates/clients/create_role.html`

```html
{% extends 'base.html' %}

{% block content %}
<div class="max-w-2xl mx-auto">
    <h1 class="text-3xl font-bold underline">Create a new Role</h1>

    {% if new_role %}
    <div class="mt-4 p-4 bg-green-100 text-green-800 border border-green-200 rounded">
        Role "{{ new_role.name }}" has been created successfully.
    </div>
    {% endif %}

    {% if form.non_field_errors %}
    <div class="mb-4 p-4 bg-red-100 text-red-800 border border-red-200 rounded">
        <ul>
            {% for error in form.non_field_errors %}
            <li>{{ error }}</li>
            {% endfor %}
        </ul>
    </div>
    {% endif %}

    <form method="post" class="mt-4">
        {% csrf_token %}
        {% for field in form %}
        <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700">{{ field.label }}</label>
            {{ field }}
            {% if field.errors %}
            <p class="text-sm text-red-500 mt-1">{{ field.errors|striptags }}</p>
            {% endif %}
        </div>
        {% endfor %}
        <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded">Submit</button>
    </form>
</div>
{% endblock %}
```

**Why:**

- Mirrors the company creation UX for the `Role` model.
- Shows success and validation feedback in a consistent way.

---

## 7. Run and test the lab

Start the server:

```bash
python manage.py runserver
```

### 7.1 Test company creation

Go to:

```text
http://127.0.0.1:8000/company/create/
```

Try:

- **Invalid cases:**
  - Name shorter than 3 characters
  - Description shorter than 30 characters
  - Duplicate email
  - Forbidden words: `spam`, `fake`, `scam`
  - Phone number with not exactly 10 digits

You should see:

- Field errors under specific fields
- Non-field errors (from `clean()`) in the red box

- **Valid case:**
  - All fields valid

You should see:

- Green success banner
- “View Company Details” link
- Clicking the link takes you to `/company/<id>/` and shows the detail page.

### 7.2 Test role creation

Go to:

```text
http://127.0.0.1:8000/role/create/
```

Try:

- Role name shorter than 4 characters → should show validation error.
- Valid role name → should show success banner.

---

## 8. What this lab teaches

By starting from your **copied Lab 11 project** and layering these changes, you learned:

- How to define models (`Company`, `Role`) and migrate them.
- How to build **ModelForms** that:
  - Map directly to models
  - Perform field-level validation (`clean_<fieldname>`)
  - Perform cross-field and database validation (`clean`)
- How to render:
  - Field errors under each field
  - Non-field errors at the top of the form
- How to:
  - Save validated data to the database
  - Redirect or re-render with success messages
  - Link to a detail view using `{% url %}` and object IDs

This lab is your first full **Model → Form → View → Template → DB → Detail** cycle—exactly the pattern used in real-world Django apps.
