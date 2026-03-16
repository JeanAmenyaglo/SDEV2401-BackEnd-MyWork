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