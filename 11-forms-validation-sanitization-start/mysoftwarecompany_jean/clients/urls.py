from django.urls import path
from .views import contact_us, newsletter

urlpatterns = [
    path("contact/", contact_us, name="contact_us"),
    path("newsletter-signup/", newsletter, name="newsletter_signup"),
]