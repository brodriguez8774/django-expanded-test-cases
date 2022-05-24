"""
Testing views for django-expanded-test-cases project.
"""

# System Imports.
from django.http import HttpResponse


def login(request):
    """"""
    return HttpResponse('Pretend this is a login page.')
