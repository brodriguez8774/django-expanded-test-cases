"""
Testing URL configuration for django-expanded-test-cases project.

Mocks being the "project settings root" urls.py file.
"""

# Third-Party Imports.
from django.urls import include, path


urlpatterns = [
    path('', (include('django_expanded_test_cases.test_urls', namespace='django_expanded_test_cases'))),
]
