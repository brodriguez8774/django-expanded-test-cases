"""
Root URL configuration for django-expanded-test-cases project UnitTests.

Mocks being the "project settings root" urls.py file.
"""

# Third-Party Imports.
from django.urls import include, path


urlpatterns = [
    path('', (include('tests.django_expanded_test_cases.testing.app_urls', namespace='django_expanded_test_cases'))),
]
