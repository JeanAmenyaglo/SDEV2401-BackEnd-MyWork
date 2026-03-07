## 1. Project setup

### 1.1. Create project folder and virtual environment

In your terminal (PowerShell):

```powershell
cd "C:\Users\jeana\Desktop\NAIT\Term_2\SDEV 2401 Rapid Backend Application Development\SDEV2401-Backend-MyWork\3-intro-blog-example-continued-start"
mkdir myblogwebsite_jean
cd myblogwebsite_jean
python -m venv venv
.\venv\Scripts\activate
```

**Why:**  
- The `myblogwebsite_jean` folder is your project root.  
- The `venv` keeps dependencies isolated for this project only.

### 1.2. Install Django and freeze dependencies

```powershell
pip install django==5.2
pip freeze > requirements.txt
```

**Why:**  
- Installs a specific Django version so behavior is predictable.  
- `requirements.txt` records dependencies so you can recreate the environment later.

---

## 2. Create the Django project

### 2.1. Start the project

From inside `myblogwebsite_jean`:

```powershell
django-admin startproject myblogwebsite_jean .
```

**Why:**  
- Creates the Django project **in the current folder** (note the `.`).  
- Generates `manage.py` and the inner `myblogwebsite_jean` config package.

You should now see:

- `manage.py`  
- `myblogwebsite_jean/` (inner folder with settings, urls, etc.)  
- `venv/`  
- `requirements.txt`

### 2.2. Run initial server check

```powershell
python manage.py runserver
```

Open `http://127.0.0.1:8000/` — you should see the Django welcome page.

**Why:**  
- Confirms Django is installed and the project is wired correctly.  
- If this fails, fix it before adding more complexity.

---

## 3. Create the blog app

### 3.1. Start the app

Stop the server (CTRL+C), then:

```powershell
python manage.py startapp blog
```

**Why:**  
- Apps are modular units of functionality.  
- `blog` will contain models, views, templates, and URLs for your blog feature.

You now have a `blog/` folder.

### 3.2. Register the app in settings

Open:

```text
myblogwebsite_jean/settings.py
```

Find `INSTALLED_APPS` and add `'blog',`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
]
```

**Why:**  
- Tells Django to include the `blog` app in the project.  
- Without this, migrations and templates for `blog` won’t be recognized.

---

## 4. Define the Post model

### 4.1. Create the model

Open:

```text
blog/models.py
```

Replace contents with:

```python
from django.conf import settings
from django.db import models
from django.utils import timezone

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

**Why:**  
- `Post` defines the structure of a blog post in the database.  
- `author` links to a user; `title` and `text` store content; dates track creation/publishing.  
- `publish()` is a helper method; `__str__` makes admin display readable.

### 4.2. Create migrations and apply them

```powershell
python manage.py makemigrations
python manage.py migrate
```

**Why:**  
- `makemigrations` generates migration files from model changes.  
- `migrate` applies them to the database, creating the `Post` table.

---

## 5. Admin setup

### 5.1. Create a superuser

```powershell
python manage.py createsuperuser
```

Follow prompts for username, email, password.

**Why:**  
- Allows you to log into `/admin` and manage posts via a UI.

### 5.2. Register the Post model in admin

Open:

```text
blog/admin.py
```

Add:

```python
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```

**Why:**  
- Makes `Post` appear in the Django admin interface.

---

## 6. Views and URLs — list page

### 6.1. Create the list view

Open:

```text
blog/views.py
```

Replace contents with:

```python
from django.shortcuts import render, get_object_or_404
from .models import Post

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/posts_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
```

**Why:**  
- `post_list` loads all posts and passes them to a template.  
- `post_detail` will be used later for the detail page.  
- Keeping both here avoids the “no attribute post_list” error we hit earlier.

### 6.2. App URLs

Create:

```text
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

**Why:**  
- Maps URLs to view functions.  
- `''` → homepage list; `post/<int:pk>/` → detail page for a specific post.

### 6.3. Project URLs

Open:

```text
myblogwebsite_jean/urls.py
```

Update to include `blog.urls`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]
```

**Why:**  
- Routes the root URL (`/`) to the `blog` app.  
- Keeps URL configuration modular.

---

## 7. Templates — list page

### 7.1. Create template folders

Create folders:

```text
blog/templates/blog/
```

Inside `blog/templates/blog/`, create:

```text
posts_list.html
```

### 7.2. posts_list.html content

```html
<!doctype html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <title>Django, posts app</title>
  </head>
  <body>
    <div class="max-w-2xl mx-auto">
        <h1 class="text-3xl font-bold underline">
          Hello, I'm using a backend framework!
        </h1>

        {% for post in posts %}
            <div class="bg-white shadow rounded-xl p-4 mb-4">
                <a href="{% url 'post_detail' post.pk %}">
                    <p class="text-lg mb-2">{{ post.title }}</p>
                </a>
                <span class="text-sm text-gray-500">{{ post.created_date }}</span>
            </div>
        {% endfor %}
    </div>
  </body>
</html>
```

**Why:**  
- Uses the `posts` context from `post_list` view.  
- Loops over posts and displays title + created date.  
- Links each title to its detail page using the URL name `post_detail`.

---

## 8. Templates — detail page

### 8.1. Create post_detail.html

In the same folder (`blog/templates/blog/`), create:

```text
post_detail.html
```

Add:

```html
<!doctype html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <title>{{ post.title }}</title>
  </head>
  <body>
    <div class="max-w-2xl mx-auto">
        <div class="max-w-3xl mx-auto mt-10 p-6 bg-white shadow-md rounded-lg">
            <h1 class="text-3xl font-bold text-gray-800 mb-4">{{ post.title }}</h1>
            <p class="text-sm text-gray-500 mb-6">Posted on {{ post.created_date }}</p>

            <div class="prose prose-lg text-gray-700">
                {{ post.text|linebreaks }}
            </div>
        </div>
    </div>
  </body>
</html>
```

**Why:**  
- Uses the `post` context from `post_detail` view.  
- Displays full content of a single post.  
- `|linebreaks` converts newlines in text to HTML paragraphs.

---

## 9. Using the admin to create posts

### 9.1. Run the server

```powershell
python manage.py runserver
```

### 9.2. Add posts

- Go to `http://localhost:8000/admin`  
- Log in with your superuser  
- Click **Posts** → **Add Post**  
- Fill in `title` and `text`  
- Save

### 9.3. View posts

- Go to `http://localhost:8000/`  
- You should see your posts listed  
- Click a title → you should see the detail page

**Why:**  
- Confirms the full flow: model → admin → view → template → browser.

---

## 10. Common issues we hit (and how to fix them)

### 10.1. “can’t open file manage.py: No such file or directory”

**Cause:**  
Running `python manage.py ...` from the wrong folder.

**Fix:**  
- Make sure you are in the folder that contains `manage.py`:

```powershell
cd C:\Users\jeana\Desktop\NAIT\Term_2\SDEV 2401 Rapid Backend Application Development\SDEV2401-Backend-MyWork\3-intro-blog-example-continued-start\myblogwebsite_jean
dir
```

You should see `manage.py` in the output.  
Then run:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### 10.2. `AttributeError: module 'blog.views' has no attribute 'post_list'`

**Cause:**  
`blog/urls.py` references `views.post_list`, but `post_list` is missing from `blog/views.py`.

**Fix:**  
Ensure `blog/views.py` contains:

```python
from django.shortcuts import render, get_object_or_404
from .models import Post

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/posts_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
```

**Why this matters:**  
- Django imports `blog.views` when resolving URLs.  
- If the function referenced in `urls.py` doesn’t exist, you get this error.

---

## 11. Mental model recap

You can always come back to this core flow:

```text
Browser → URL → View → Model → View → Template → Browser
```

- **URL**: decides which view to call (`blog/urls.py`, `myblogwebsite_jean/urls.py`)  
- **View**: Python function that loads data (`post_list`, `post_detail`)  
- **Model**: database structure (`Post`)  
- **Template**: HTML that renders the data (`posts_list.html`, `post_detail.html`)  