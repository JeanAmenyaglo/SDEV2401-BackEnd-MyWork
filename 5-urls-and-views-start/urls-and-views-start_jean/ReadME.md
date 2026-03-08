# 📘 **Django URLs & Views Fundamentals — Pet Adoption Lab**  
*A clean, structured README documenting the full lab you completed.*

---

## 🐾 **Overview**

This lab introduces the **core Django request–response cycle**, using a simple “Pet Adoption” app to demonstrate:

- Project vs. App structure  
- URL routing  
- Views and dynamic parameters  
- Passing data from Python to templates  
- Template loops and conditionals  
- Error handling  
- Filtering data based on URL input  

This is the foundational architecture every Django backend engineer must master before moving on to models, forms, authentication, and databases.

---

## 🧠 **Django Architecture (Mental Model Diagram)**

```
┌──────────────────────────────────────────────────────────────┐
│                        DJANGO PROJECT                         │
│  (The whole website: settings, database, global URLs)         │
│                                                              │
│  urls_views_fundamentals/                                    │
│      ├── settings.py   ← global configuration                 │
│      ├── urls.py       ← master URL router                    │
│      └── ...                                                    │
└──────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                           APP                                │
│                 (A feature inside the project)               │
│                                                              │
│  pet_adoption/                                               │
│      ├── views.py      ← logic: gets data, chooses template  │
│      ├── urls.py       ← app-specific URL routes             │
│      ├── templates/    ← HTML pages                          │
│      │     └── pet_adoption/                                 │
│      │           ├── home_page.html                          │
│      │           ├── pet_details.html                        │
│      │           └── pets_for_lifestyle.html                 │
│      └── ...                                                 │
└──────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                     REQUEST FLOW (The Pipeline)              │
│                                                              │
│  1. Browser requests URL                                      │
│        ↓                                                      │
│  2. Project urls.py checks patterns                           │
│        ↓                                                      │
│  3. Includes app urls.py                                      │
│        ↓                                                      │
│  4. App urls.py matches a specific route                      │
│        ↓                                                      │
│  5. Calls the correct view function                           │
│        ↓                                                      │
│  6. View prepares data (context)                              │
│        ↓                                                      │
│  7. View renders a template with that data                    │
│        ↓                                                      │
│  8. Browser displays the final HTML page                      │
└──────────────────────────────────────────────────────────────┘
```

---

## 📁 **Project Structure**

```
urls-and-views-start_jean/
│
├── manage.py
├── urls_views_fundamentals/        ← Project folder
│     ├── settings.py
│     ├── urls.py
│     └── ...
│
└── pet_adoption/                   ← App folder
      ├── views.py
      ├── urls.py
      ├── templates/
      │     └── pet_adoption/
      │           ├── home_page.html
      │           ├── pet_details.html
      │           └── pets_for_lifestyle.html
      └── ...
```

---

## 🧩 **Step-by-Step Summary**

### **1. Create Django Project**
```bash
django-admin startproject urls_views_fundamentals
```

### **2. Create App**
```bash
python manage.py startapp pet_adoption
```

### **3. Register App in `settings.py`**
```python
INSTALLED_APPS = [
    ...
    "pet_adoption",
]
```

---

## 🏠 **Home Page**

### **View (`views.py`)**
```python
from django.shortcuts import render

PET_TYPES = {
    'dog': {
        'name': 'Dog',
        'traits': 'Loyal, energetic, needs space and exercise.',
        'lifestyle_fit': 'active'
    },
    'cat': {
        'name': 'Cat',
        'traits': 'Independent, cuddly, low-maintenance.',
        'lifestyle_fit': 'quiet'
    },
    'rabbit': {
        'name': 'Rabbit',
        'traits': 'Gentle, small, requires calm environment.',
        'lifestyle_fit': 'quiet'
    },
    'parrot': {
        'name': 'Parrot',
        'traits': 'Social, intelligent, needs stimulation.',
        'lifestyle_fit': 'social'
    }
}

def home_page(request):
    return render(request, "pet_adoption/home_page.html", {"pet_types": PET_TYPES})
```

### **Template Loop (`home_page.html`)**
```html
{% for pet_type, pet in pet_types.items %}
    <li>
        <strong>{{ pet_type }}</strong> — {{ pet.traits }}
    </li>
{% endfor %}
```

---

## 🐶 **Pet Details Page**

### **Dynamic URL (`pet_adoption/urls.py`)**
```python
path("pet_type/<str:pet_type>/", pet_type_details, name="pet_type_details"),
```

### **View**
```python
def pet_type_details(request, pet_type):
    pet_data = PET_TYPES.get(pet_type, None)

    context = {
        "pet_type": pet_type,
        "pet_data": pet_data,
    }

    return render(request, "pet_adoption/pet_details.html", context)
```

### **Template with Conditional**
```html
{% if pet_data %}
    <p>The traits of a {{ pet_type }} are: {{ pet_data.traits }}</p>
{% else %}
    <p>Sorry, we don't have information about this pet type.</p>
{% endif %}
```

---

## 🎯 **Challenge: Pets by Lifestyle**

### **URL**
```python
path("pets_for_lifestyle/<str:lifestyle_fit>/", pets_for_lifestyle),
```

### **View**
```python
def pets_for_lifestyle(request, lifestyle_fit):

    matching_pets = {
        key: pet
        for key, pet in PET_TYPES.items()
        if pet["lifestyle_fit"] == lifestyle_fit
    }

    context = {
        "lifestyle_fit": lifestyle_fit,
        "matching_pets": matching_pets,
    }

    return render(request, "pet_adoption/pets_for_lifestyle.html", context)
```

### **Template**
```html
{% if matching_pets %}
    {% for pet_key, pet in matching_pets.items %}
        <li>{{ pet.name }} — {{ pet.traits }}</li>
    {% endfor %}
{% else %}
    <p>No pets match this lifestyle.</p>
{% endif %}
```

---

## ✅ **What You Learned**

- Django project vs. app architecture  
- Template folder structure  
- URL routing (project-level + app-level)  
- Dynamic URL parameters  
- Passing context from views to templates  
- Template loops and conditionals  
- Error handling  
- Filtering data dynamically  

This is the **core foundation** of Django backend development.

