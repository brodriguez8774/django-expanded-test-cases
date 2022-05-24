"""
Testing URL configuration for django-expanded-test-cases project.

Mocks being the "project settings root" urls.py file.
"""

# System Imports.
from django.urls import include, path


app_name = 'expanded_test_cases'
urlpatterns = [
    path('', (include('tests.urls_app', namespace='expanded_test_cases'))),
]
