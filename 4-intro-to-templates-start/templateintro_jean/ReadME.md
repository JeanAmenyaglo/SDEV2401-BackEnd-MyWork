# **Intro to Template Fundamentals — Lab README**  
### *Using Django’s Template Engine Inside the Django Shell*

---

## ⭐ **1. Overview**

This lab introduces the fundamentals of Django’s template engine (Jinja‑like syntax) using the Django shell.  
You will learn how to:

- Render variables  
- Loop through lists  
- Use loop counters  
- Apply conditionals  
- Apply template filters  
- Debug template context  

All template rendering happens **inside the Django shell**, not in HTML files or views.

---

## ⭐ **2. Prerequisites**

Before starting, ensure you have:

- Python installed  
- A virtual environment created  
- Django installed inside the virtual environment  
- A Django project created (with `manage.py` present)

---

## ⭐ **3. Activate Virtual Environment**

From your project folder:

```powershell
.\venv\Scripts\activate
```

Confirm activation by checking that your terminal shows:

```
(venv)
```

---

## ⭐ **4. Navigate to the Django Project Root**

This is the folder that contains:

```
manage.py
```

Example:

```
4-intro-to-templates-start\templateintro_jean
```

---

## ⭐ **5. Open the Django Shell**

Run:

```powershell
python manage.py shell
```

You should see:

```
(InteractiveConsole)
>>>
```

This is where all template code will run.

---

## ⭐ **6. Import the Template Engine**

Inside the Django shell:

```python
from django.template import Template, Context
```

---

## ⭐ **7. Render Your First Template**

### **Step 1 — Create a data dictionary**

```python
data = {
    "rating_topic": "movie",
    "best_rating": 10,
    "worst_rating": 0,
}
```

### **Step 2 — Create a template**

```python
template = Template("""
{{ rating_topic }} ratings from {{ worst_rating }} to {{ best_rating }}
""")
```

### **Step 3 — Render**

```python
context = Context(data)
print(template.render(context))
```

**Expected Output:**

```
movie ratings from 0 to 10
```

---

## ⭐ **8. Loop Through a List**

Update your data:

```python
data = {
    "rating_topic": "Book",
    "best_rating": 5,
    "worst_rating": 1,
    "items": [
        {"title": "Brave New World", "rating": 4},
        {"title": "1984", "rating": 5},
        {"title": "The Great Gatsby", "rating": 4},
        {"title": "Twilight", "rating": 1},
    ]
}
```

Create a template with a loop:

```python
template = Template("""
{{ rating_topic }} ratings from {{ worst_rating }} to {{ best_rating }}

{% for item in items %}
    {{ item.title }} - {{ item.rating }}
{% endfor %}
""")
```

Render:

```python
print(template.render(Context(data)))
```

---

## ⭐ **9. Add Loop Counters**

```python
template = Template("""
{{ rating_topic }} ratings from {{ worst_rating }} to {{ best_rating }}

{% for item in items %}
    {{ forloop.counter }}. {{ item.title }} - {{ item.rating }}
{% endfor %}
""")
```

Render:

```python
print(template.render(Context(data)))
```

---

## ⭐ **10. Add Conditionals**

```python
template = Template("""
{{ rating_topic }} ratings from {{ worst_rating }} to {{ best_rating }}

{% for item in items %}
    {% if item.rating == best_rating %}
        ⭐ {{ forloop.counter }}. {{ item.title }} - {{ item.rating }} (Top Rated)
    {% elif item.rating == worst_rating %}
        ⚠️ {{ forloop.counter }}. {{ item.title }} - {{ item.rating }} (Lowest Rated)
    {% else %}
        {{ forloop.counter }}. {{ item.title }} - {{ item.rating }}
    {% endif %}
{% endfor %}
""")
```

Render:

```python
print(template.render(Context(data)))
```

---

## ⭐ **11. Apply Template Filters**

### Uppercase:

```python
template = Template("{{ rating_topic|upper }}")
```

### Lowercase:

```python
template = Template("{{ rating_topic|lower }}")
```

### Length:

```python
template = Template("There are {{ items|length }} items.")
```

Render each using:

```python
print(template.render(Context(data)))
```

---

## ⭐ **12. Debug the Template Context**

```python
template = Template("""
{% debug %}
""")
```

Render:

```python
print(template.render(Context(data)))
```

This prints all variables available in the template.

---

## ⭐ **13. Final Combined Template (Everything Together)**

```python
template = Template("""
{{ rating_topic|upper }} RATINGS ({{ items|length }} items)

{% for item in items %}
    {% if item.rating == best_rating %}
        ⭐ {{ forloop.counter }}. {{ item.title|upper }} - {{ item.rating }} (TOP)
    {% elif item.rating == worst_rating %}
        ⚠️ {{ forloop.counter }}. {{ item.title|lower }} - {{ item.rating }} (LOWEST)
    {% else %}
        {{ forloop.counter }}. {{ item.title }} - {{ item.rating }}
    {% endif %}
{% endfor %}
""")
```

Render:

```python
print(template.render(Context(data)))
```

---

## ⭐ **14. Summary**

In this lab, you learned how to:

- Use Django’s template engine inside the Django shell  
- Render variables  
- Loop through lists  
- Use loop counters  
- Apply conditionals  
- Apply filters  
- Debug template context  

This foundational knowledge prepares you for:

- Django views  
- HTML templates  
- Template inheritance  
- Real-world rendering logic  