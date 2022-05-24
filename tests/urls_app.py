"""
Testing URL configuration for django-expanded-test-cases project.

Mocks being an "app" urls.py file.
"""

# System Imports.
from django.urls import path

# User Imports.
from . import views


app_name = 'expanded_test_cases'
urlpatterns = [
    path('', views.login, name='login')
]
