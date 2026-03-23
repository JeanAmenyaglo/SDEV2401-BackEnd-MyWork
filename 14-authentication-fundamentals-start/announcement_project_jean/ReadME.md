
# 📘 **Announcements Project — Full Build Guide (Step‑by‑Step README)**

This project implements a complete authentication system in Django using:

- A **custom user model** with roles (teacher, student)  
- Registration, login, logout  
- Role‑based access (teachers can create announcements)  
- Protected views using `@login_required`  
- Templates for all pages  
- A clean navigation bar that changes based on authentication state  

This README explains **every step**, **every file**, and **why each part is needed**.

---

# 🏗️ 1. **Project Setup**

### Create the Django project:
```bash
django-admin startproject announcements_project
```

This creates:

```
announcements_project/
    announcements_project/
        settings.py
        urls.py
        wsgi.py
    manage.py
```

### Create the core app (for authentication)
```bash
python manage.py startapp core
```

### Create the announcements app
```bash
python manage.py startapp announcements
```

### Add apps to `INSTALLED_APPS`
In `announcements_project/settings.py`:

```python
INSTALLED_APPS = [
    ...
    'core',
    'announcements',
]
```

---

# 🔐 2. **Custom User Model (core app)**

Django recommends creating a custom user model **at the start of a project** so you can add fields later.

### Why do we need a custom user model?
- We need a **role** field (teacher or student)
- Django’s default user model cannot be modified after migrations
- Role-based access requires storing the user’s role

### Create the model in `core/models.py`:
```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"
```

### Tell Django to use this model
In `settings.py`:

```python
AUTH_USER_MODEL = 'core.User'
```

### Register the model in admin
`core/admin.py`:

```python
from django.contrib import admin
from .models import User

admin.site.register(User)
```

### Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create a superuser
```bash
python manage.py createsuperuser
```

Then log in at `/admin/` and assign a role.

---

# 🧩 3. **Announcements App Structure**

The announcements app contains:

### `models.py`
Defines the Announcement model:

```python
class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
```

### `forms.py`
We create a ModelForm so Django can automatically generate a form:

```python
from django import forms
from .models import Announcement

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'message']
```

### Why do we need forms?
- They validate user input
- They prevent security issues
- They automatically generate HTML form fields

---

# 🧑‍🏫 4. **Registration System**

### Create `core/forms.py`
We extend Django’s secure `UserCreationForm`:

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']
```

### Create the registration view
`core/views.py`:

```python
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegistrationForm

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("announcement_list")
    else:
        form = UserRegistrationForm()
    return render(request, "core/register.html", {"form": form})
```

### Add registration URL
`core/urls.py`:

```python
from django.urls import path
from .views import register

urlpatterns = [
    path("register/", register, name="register"),
]
```

### Include core URLs in project URLs
`announcements_project/urls.py`:

```python
path('accounts/', include('core.urls')),
```

---

# 🔑 5. **Login & Logout**

### Use Django’s built‑in authentication views
In `core/urls.py`:

```python
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="core/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
```

### Add redirect settings
In `settings.py`:

```python
LOGIN_REDIRECT_URL = '/announcements/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
LOGIN_URL = '/accounts/login/'
```

---

# 📢 6. **Announcements Views**

### Add login protection
`announcements/views.py`:

```python
from django.contrib.auth.decorators import login_required

@login_required
def announcement_list(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, "announcements/announcement_list.html", {"announcements": announcements})
```

### Create announcement view (teacher only)
```python
@login_required
def create_announcement(request):
    if request.user.role != "teacher":
        return redirect("announcement_list")

    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()
            return redirect("announcement_list")
    else:
        form = AnnouncementForm()

    return render(request, "announcements/create_announcement.html", {"form": form})
```

### Add URLs
`announcements/urls.py`:

```python
urlpatterns = [
    path("", announcement_list, name="announcement_list"),
    path("create/", create_announcement, name="create_announcement"),
]
```

### Include in project URLs
`announcements_project/urls.py`:

```python
path('announcements/', include('announcements.urls')),
```

---

# 🎨 7. **Templates (All HTML Files)**

### `templates/base.html`
Contains navigation bar with login/logout/register links and user info.

### `templates/core/login.html`
Login form.

### `templates/core/register.html`
Registration form.

### `templates/announcements/announcement_list.html`
Displays all announcements.

### `templates/announcements/create_announcement.html`
Form for teachers to create announcements.

---

# 🔒 8. **Restricting Access**

We use:

```python
@login_required
```

This ensures:

- Only logged‑in users can view announcements
- Only teachers can create announcements

---

# 🧪 9. **Testing Checklist**

- Register a student  
- Register a teacher  
- Login  
- Logout  
- Teacher creates announcements  
- Student can view but not create  
- Navigation bar updates based on authentication  
- Admin panel shows users and announcements  

---

# 🎉 **Project Completed**