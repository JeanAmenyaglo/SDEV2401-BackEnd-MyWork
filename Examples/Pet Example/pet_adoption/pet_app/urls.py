from django.urls import path
from .views import home_page, pet_type_details, pets_for_lifestyle, test_template
urlpatterns = [
    path("", home_page, name="home_page"),
    #detail page
    path("pets/<str:pet_type>/", pet_type_details, name="pet_type_details"),
    path("pets_for_lifestyle/<str:lifestyle>/", pets_for_lifestyle, name="pets_for_lifestyle"),
    path("test-template/", test_template, name="test_template"),
]