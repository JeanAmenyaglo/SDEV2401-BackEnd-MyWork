
# 🟦 **1. Create a New Project Directory**

Open a terminal and create a new folder:

```
mkdir forms-lab
cd forms-lab
```

---

# 🟩 **2. Create and Activate a Virtual Environment**

```
python -m venv venv
```

Activate it:

### Windows:
```
venv\Scripts\activate
```

---

# 🟧 **3. Install Django**

```
pip install django
```

---

# 🟨 **4. Create a New Django Project**

```
django-admin startproject mysoftwarecompany_jean .
```

This creates:

```
manage.py
mysoftwarecompany_jean/
```

---

# 🟪 **5. Create the `clients` App**

```
python manage.py startapp clients
```

Add `"clients"` to `INSTALLED_APPS` in:

```
mysoftwarecompany_jean/settings.py
```

---

# 🟫 **6. Create the Global Templates Directory**

At the project root (same level as manage.py):

```
mkdir templates
```

Create:

```
templates/base.html
```

Add a simple layout:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Software Company</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100">

<nav class="bg-blue-600 text-white px-6 py-4">
    <h1 class="text-xl font-bold">My Software Company</h1>
</nav>

<main class="p-6">
    {% block content %}{% endblock %}
</main>

</body>
</html>
```

---

# 🟦 **7. Configure Django to Use the Templates Directory**

In `mysoftwarecompany_jean/settings.py`, update:

```python
'DIRS': [BASE_DIR / "templates"],
```

---

# 🟩 **8. Create Forms**

Open:

```
clients/forms.py
```

Add:

```python
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long.")
        return name

    def clean_message(self):
        message = self.cleaned_data.get("message")
        if len(message) < 10:
            raise forms.ValidationError("Message must be at least 10 characters long.")
        return message


class NewsletterSignupForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long.")
        return name
```

---

# 🟧 **9. Create Views**

Open:

```
clients/views.py
```

Add:

```python
from django.shortcuts import render
from django.core.mail import send_mail
from .forms import ContactForm, NewsletterSignupForm


def contact_us(request):
    if request.method == "GET":
        form = ContactForm()
        return render(request, "clients/contact_us.html", {"form": form})

    elif request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            send_mail(
                subject=f"New contact us message from {name}",
                message=message,
                from_email=email,
                recipient_list=["some_admin_account@test.com"],
            )

            return render(
                request,
                "clients/contact_us.html",
                {"form": ContactForm(), "success": True},
            )

        return render(request, "clients/contact_us.html", {"form": form})


def newsletter(request):
    if request.method == "GET":
        form = NewsletterSignupForm()
        return render(request, "clients/newsletter_signup.html", {"form": form})

    elif request.method == "POST":
        form = NewsletterSignupForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]

            send_mail(
                subject="Newsletter Signup Confirmation",
                message=f"Hi {name},\n\nThank you for signing up for our newsletter!",
                from_email="no-reply@mysoftwarecompany.com",
                recipient_list=[email],
            )

            return render(
                request,
                "clients/newsletter_signup.html",
                {"form": NewsletterSignupForm(), "success": True},
            )

        return render(request, "clients/newsletter_signup.html", {"form": form})
```

---

# 🟨 **10. Create URL Routes**

Create:

```
clients/urls.py
```

Add:

```python
from django.urls import path
from .views import contact_us, newsletter

urlpatterns = [
    path("contact/", contact_us, name="contact_us"),
    path("newsletter-signup/", newsletter, name="newsletter_signup"),
]
```

Then include it in:

```
mysoftwarecompany_jean/urls.py
```

Add:

```python
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("clients.urls")),
]
```

---

# 🟪 **11. Create Templates for Each Form**

### Contact Form Template

Create:

```
clients/templates/clients/contact_us.html
```

Add:

```html
{% extends 'base.html' %}

{% block content %}
<div class="max-w-2xl mx-auto">
    <h1 class="text-3xl font-bold underline">Contact Us</h1>

    {% if success %}
    <div class="mt-4 p-4 bg-green-100 text-green-800 border border-green-200 rounded">
        Your message has been sent successfully.
    </div>
    {% endif %}

    <form method="post" class="mt-4">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded">Submit</button>
    </form>
</div>
{% endblock %}
```

### Newsletter Signup Template

Create:

```
clients/templates/clients/newsletter_signup.html
```

Add:

```html
{% extends 'base.html' %}

{% block content %}
<div class="max-w-2xl mx-auto">
    <h1 class="text-3xl font-bold underline">Newsletter Signup</h1>

    {% if success %}
    <div class="mt-4 p-4 bg-green-100 text-green-800 border border-green-200 rounded">
        Thank you for signing up! A confirmation email has been sent.
    </div>
    {% endif %}

    <form method="post" class="mt-4">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded">Sign Up</button>
    </form>
</div>
{% endblock %}
```

---

# 🟫 **12. Configure Email Backend**

In `settings.py`, add:

```python
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

This prints emails to the terminal.

---

# 🟦 **13. Run Migrations**

```
python manage.py migrate
```

---

# 🟩 **14. Start the Server**

```
python manage.py runserver
```

Visit:

- Contact form → [http://127.0.0.1:8000/contact/](http://127.0.0.1:8000/contact/)  
- Newsletter signup → `http://127.0.0.1:8000/newsletter-signup/` [(127.0.0.1 in Bing)](https://www.bing.com/search?q="http%3A%2F%2F127.0.0.1%3A8000%2Fnewsletter-signup%2F")  

Submit forms and check the console for emails.