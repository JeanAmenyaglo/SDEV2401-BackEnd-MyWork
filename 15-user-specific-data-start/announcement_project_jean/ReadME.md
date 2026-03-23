
# #️⃣ **Authentication with Authorization & User‑Specific Data** 

---

# 📌 **Overview**

In this lab, we extended our existing Django authentication system by adding **authorization**, **role‑based access control**, **permissions**, and **user‑specific data handling**.  
This lab builds directly on the previous announcements project, using the same custom User model with `role` (Teacher/Student).

We implemented:

- Role‑based access control (RBAC)  
- Permission‑based access control using Django’s built‑in system  
- A teacher‑only “Create Announcement” workflow  
- User‑specific data via `created_by`  
- Custom 403 Forbidden error page  
- Template‑level permission checks  

This lab demonstrates how Django handles **authentication (who you are)** and **authorization (what you can do)**.

---

# 🧱 **Project Structure (Inherited from Lab 1)**

```
announcements/
announcements_project/
core/
templates/
manage.py
db.sqlite3
```

We continued using:

- Custom User model (`core/models.py`)
- Announcements app
- Authentication system (register, login, logout)
- Base templates and URL structure

---

# ✅ **Step‑by‑Step Implementation**

---

## **1. Role‑Based Authorization with `is_teacher`**

We created a helper function to check if a user is a teacher.

```python
def is_teacher(user):
    return user.role == 'teacher'
```

---

## **2. Restricting Access with `user_passes_test`**

Initially, we restricted the create view so only teachers could access it.

```python
@login_required
@user_passes_test(is_teacher, login_url='login')
def create_announcement(request):
    ...
```

---

## **3. Updated Create Announcement Template**

We added a full form rendering with labels, errors, and CSRF protection.

```html
<form method="post">
    {% csrf_token %}
    {% for field in form %}
        <label>{{ field.label }}</label>
        {{ field }}
    {% endfor %}
    <button type="submit">Create Announcement</button>
</form>
```

---

## **4. Saving User‑Specific Data (`created_by`)**

We updated the view so each announcement is linked to the teacher who created it.

```python
announcement = form.save(commit=False)
announcement.created_by = request.user
announcement.save()
```

---

## **5. Hide “Create Announcement” Button for Students**

In `announcement_list.html`, we only show the button to teachers:

```html
{% if user.is_authenticated and user.role == 'teacher' %}
<a href="{% url 'create_announcement' %}">Create New Announcement</a>
{% endif %}
```

---

## **6. Custom 403 Forbidden Page**

We created `templates/403.html`:

```html
<h1>You don't have permission to access this page.</h1>
```

This page appears when unauthorized users try to access restricted views.

---

## **7. Permission‑Based Authorization (`permission_required`)**

We replaced role checks with Django’s built‑in permissions:

```python
@login_required
@permission_required('announcements.add_announcement', raise_exception=True)
def create_announcement(request):
    ...
```

This integrates with Django’s admin Groups & Permissions system.

---

# 🔐 **Permissions & Groups (Optional Section Completed)**

In Django admin:

### **Teacher Group**
- add_announcement  
- change_announcement  
- delete_announcement  
- view_announcement  

### **Student Group**
- view_announcement only  

Users were assigned to groups accordingly.

---

# 🧪 **Testing Summary**

### ✔ Teacher  
- Can see “Create Announcement” button  
- Can access `/announcements/create/`  
- Can create announcements  
- Announcements show correct `created_by`  

### ✔ Student  
- Cannot see “Create Announcement” button  
- Visiting `/announcements/create/` shows **403 Forbidden**  
- Can view announcements list  

Everything behaved exactly as expected.

---

# 🎯 **What I Learned**

- The difference between **authentication** and **authorization**  
- How to restrict access using:
  - `login_required`
  - `user_passes_test`
  - `permission_required`
- How to associate data with the logged‑in user  
- How to use Django’s built‑in permissions and groups  
- How to create custom error pages  
- How to hide/show UI elements based on permissions  

This lab deepened my understanding of Django’s security model and prepared me for more advanced backend development.

