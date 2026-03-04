from django.urls import path
from . import views

urlpatterns = [
    # Note: the empty string '' means the root of this app
    path('', views.post_list, name='post_list'),
    # post Detail view
    # <datatype:variable_name>
    # make sure the variable name matches the view function parameter in our views.py
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]