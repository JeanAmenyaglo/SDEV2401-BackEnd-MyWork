from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_companies, name='list_companies'),
    path('company/create/', views.create_company, name='create_company'),
    path('company/<int:company_id>/update/', views.update_company, name='update_company'),
    path('company/<int:company_id>/', views.company_detail, name='company_detail'),
    path('company/<int:company_id>/employee/add/', views.add_employee, name='add_employee'),
]