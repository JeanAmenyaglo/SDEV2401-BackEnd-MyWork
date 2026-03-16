 **🚀 How to Set Up This Lab (Step-by-Step)**

Follow these steps to set up the project from scratch.

---

## **1. Clone or Download the Starter Project**
The instructor provides a starter Django project containing:

- Project folder: `mysoftwarecompany_jean`
- App folder: `clients`
- Base template
- Companies list template
- JSON fixture files

---

## **2. Install Dependencies**
Inside the project folder:

```
pip install -r requirements.txt
```

Or manually install Django:

```
pip install django
```

---

## **3. Reset the Database (Important for This Lab)**

### **A. Delete the SQLite database**
```
del db.sqlite3
```

### **B. Delete old migrations**
Inside:

```
clients/migrations/
```

Delete everything **except**:

```
__init__.py
```

This ensures a clean schema.

---

## **4. Apply Migrations**
Rebuild the database:

```
python manage.py makemigrations
python manage.py migrate
```

This creates fresh tables for:

- Company  
- Role  
- Employee  
- Auth  
- Sessions  

---

## **5. Load the Fixture Data**
Load the main dataset:

```
python manage.py loaddata clients_data.json
```

Load the Quantum Solutions dataset:

```
python manage.py loaddata clients_data_quantum.json
```

You should see:

```
Installed X object(s) from 1 fixture(s)
```

This populates:

- 4 companies  
- 3 roles  
- 17+ employees  

---

## **6. Run the Server**
```
python manage.py runserver
```

---

## **7. Test the URLs**

### ✔ Companies List
```
http://localhost:8000/companies/
```

### ✔ Company Detail
```
http://localhost:8000/company/1/
http://localhost:8000/company/2/
http://localhost:8000/company/10/
```

### ✔ Employee Search
```
http://localhost:8000/company/1/employees/results/?q=Gary
```

Everything should now be fully functional.

---

# **🧠 What’s New in This Lab (Compared to the Previous One)**

This lab introduces several new backend concepts that were *not* part of the previous project.

---

## **1. JSON Fixtures (NEW)**  
You now load data using:

```
python manage.py loaddata <file>.json
```

This teaches:

- Automated data loading  
- Reproducible environments  
- Working with realistic datasets  

---

## **2. New Model: Role (NEW)**  
A new `Role` model was added:

```
Company ───< Employee >─── Role
```

This expands the data model beyond Lab 9.

---

## **3. Updated Employee Model (NEW Relationship)**  
Employees now reference roles:

```python
role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
```

This supports:

- Role assignments  
- Null roles (as required by fixtures)

---

## **4. Company Detail Page (NEW)**  
A new dynamic URL:

```
/company/<id>/
```

Displays:

- Company info  
- Description  
- Employees  
- Roles  

---

## **5. Employee Search (NEW)**  
A new search view:

```
/company/<id>/employees/results/?q=<name>
```

Introduces:

- Query parameters  
- ORM filtering  
- Search results templates  

---

## **6. New Templates (NEW UI Pages)**

You created:

- `company_detail.html`
- `employees_search_results.html`

These render relational data dynamically.

---

## **7. Migration Reset & Schema Alignment (NEW Workflow)**

You learned how to:

- Delete migrations  
- Rebuild the database  
- Fix schema mismatches  
- Handle `auto_now_add` migration errors  

This is real backend engineering.

---

# **📐 Final Data Model**

```
Company
    ├── name
    ├── email
    ├── description
    ├── created_at
    └── updated_at

Role
    ├── name
    ├── description
    ├── created_at
    └── updated_at

Employee
    ├── first_name
    ├── last_name
    ├── email
    ├── company (FK → Company)
    ├── role (FK → Role)
    ├── created_at
    └── updated_at
```

---

# **🧩 Views Implemented**

### **1. List Companies**
```
/companies/
```

### **2. Company Detail**
```
/company/<id>/
```

### **3. Employee Search**
```
/company/<id>/employees/results/?q=<query>
```

---

# **📁 Template Structure**

```
templates/
    base.html

clients/
    templates/
        clients/
            companies_list.html
            company_detail.html
            employees_search_results.html
```

---

# **🎯 Conclusion**

This lab transforms the simple two-model system from the previous project into a **fully relational, data-driven Django application**.  
You now understand how to:

- Design multi-table schemas  
- Load structured data  
- Build dynamic views  
- Render relational data  
- Implement search  
- Manage migrations professionally  

This is a major step toward real-world backend engineering.

