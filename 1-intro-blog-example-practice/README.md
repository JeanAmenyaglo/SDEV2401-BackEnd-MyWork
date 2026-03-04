# 🎓 Django Project Guide (Student‑Friendly Version)

This guide walks you through **every step** of building a Django project from scratch.  
Use it for assignments, labs, or your own projects.

---

# 1. Set Up Your Project Folder

Create a folder anywhere on your computer. Example:

```
myproject/
```

Open this folder in VS Code.

---

# 2. Create and Activate a Virtual Environment

A virtual environment keeps your project’s Python packages separate.

### Create the venv:

```
python -m venv venv
```

### Activate it (Windows):

```
.\venv\Scripts\activate
```

You should now see:

```
(venv)
```

at the start of your terminal line.

---

# 3. Install Django

Inside the activated venv:

```
pip install django==5.2
```

Freeze your dependencies:

```
pip freeze > requirements.txt
```

---

# 4. Create Your Django Project

Run:

```
django-admin startproject myproject
```

Your folder now looks like:

```
myproject/
    manage.py
    myproject/
        settings.py
        urls.py
```

Move into the project folder:

```
cd myproject
```

---

# 5. Create a Django App

Apps are where your actual code lives.

```
python manage.py startapp blog
```

Your structure now:

```
blog/
    models.py
    views.py
    admin.py
    urls.py (you will create this)
```

---

# 6. Add the App to Django Settings

Open:

```
myproject/settings.py
```

Find `INSTALLED_APPS` and add:

```python
'blog',
```

---

# 7. Create Your Model (Database Table)

Open:

```
blog/models.py
```

Add a simple Post model:

```python
from django.db import models
from django.utils import timezone
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
```

---

# 8. Make and Apply Migrations

These commands create the database tables.

### Create migration files:

```
python manage.py makemigrations
```

### Apply them:

```
python manage.py migrate
```

---

# 9. Create an Admin User

This lets you log into Django’s admin panel.

```
python manage.py createsuperuser
```

Enter:

- username  
- email (optional)  
- password  

---

# 10. Register Your Model in the Admin

Open:

```
blog/admin.py
```

Add:

```python
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```

Now your Post model will appear in the admin dashboard.

---

# 11. Create Your Views

Open:

```
blog/views.py
```

Add:

```python
from django.shortcuts import render, get_object_or_404
from .models import Post

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
```

---

# 12. Set Up URLs

## 12.1. Create `blog/urls.py`

Create the file:

```
blog/urls.py
```

Add:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]
```

## 12.2. Connect App URLs to Project URLs

Open:

```
myproject/urls.py
```

Add:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # blog is the homepage
]
```

---

# 13. Create Templates

Inside your blog app, create:

```
blog/
    templates/
        blog/
            post_list.html
            post_detail.html
```

### `post_list.html`

```html
<h1>My Blog Posts</h1>

{% for post in posts %}
    <h2>
        <a href="{% url 'post_detail' pk=post.pk %}">
            {{ post.title }}
        </a>
    </h2>
    <p>{{ post.published_date }}</p>
{% empty %}
    <p>No posts yet.</p>
{% endfor %}
```

### `post_detail.html`

```html
<h1>{{ post.title }}</h1>
<p>{{ post.published_date }}</p>
<p>{{ post.text }}</p>

<a href="{% url 'post_list' %}">Back to posts</a>
```

---

# 14. Run the Server

```
python manage.py runserver
```

Visit:

```
http://127.0.0.1:8000/
```

You should now see your blog homepage.

---

# 15. Add Posts Through the Admin

Go to:

```
http://127.0.0.1:8000/admin/
```

Log in with your superuser account.

Create a few posts.

Refresh the homepage — they should appear.

