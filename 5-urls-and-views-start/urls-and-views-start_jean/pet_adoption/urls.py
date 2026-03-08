from django.urls import path
from .views import home_page, pet_type_details, pets_for_lifestyle

urlpatterns = [
    path("", home_page, name="home_page"),
    path("pet_type/<str:pet_type>/", pet_type_details, name="pet_type_details"),
    path("pets_for_lifestyle/<str:lifestyle_fit>/", pets_for_lifestyle, name="pets_for_lifestyle"),
]