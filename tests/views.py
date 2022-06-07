"""
Testing views for django-expanded-test-cases project.
"""

# System Imports.
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse


def index(request):
    """"""
    # Render response.
    return render(request, 'django_expanded_test_cases/index.html', {
        'header': 'Home Page',
        'text': 'Pretend this is the project landing page.',
    })


def template_response_index(request):
    """"""
    # Render response.
    return render(request, 'django_expanded_test_cases/index.html', {
        'header': 'Home Page',
        'text': 'Pretend this is the project landing page.',
    })


def login(request):
    """"""
    # Render response.
    return render(request, 'django_expanded_test_cases/index.html', {
        'header': 'Login Page',
        'text': 'Pretend this is a login page.',
    })


def view_with_one_message(request):
    """"""
    messages.info(request, 'This is a test message.')

    # Render response.
    return render(request, 'django_expanded_test_cases/index.html', {
        'header': 'View with One Message',
        'text': (
            'Pretend useful stuff is displayed here, for one-message render() view.'
        )
    })


def view_with_two_messages(request):
    """"""
    messages.info(request, 'Test message #1.')
    messages.warning(request, 'Test message #2.')

    # Render response.
    return render(request, 'django_expanded_test_cases/index.html', {
        'header': 'View with Two Messages',
        'text': (
            'Pretend useful stuff is displayed here, for two-message render() view.'
        )
    })


def view_with_three_messages(request):
    """"""
    messages.info(request, 'Test info message.')
    messages.warning(request, 'Test warning message.')
    messages.error(request, 'Test error message.')

    # Render response.
    return render(request, 'django_expanded_test_cases/index.html', {
        'header': 'View with Three Messages',
        'text': (
            'Pretend useful stuff is displayed here, for three-message render() view.'
        )
    })


def template_response_with_three_messages(request):
    """"""
    messages.info(request, 'Test info message.')
    messages.warning(request, 'Test warning message.')
    messages.error(request, 'Test error message.')

    # Render response.
    return TemplateResponse(request, 'django_expanded_test_cases/index.html', {
        'header': 'View with Three Messages',
        'text': (
            'Pretend useful stuff is displayed here, for three-message TemplateResponse view.'
        )
    })


def user_detail(request, pk):
    """"""
    # Pull database info.
    user = get_object_or_404(get_user_model(), pk=pk)

    # Render response.
    return render(request, 'django_expanded_test_cases/index.html', {
        'header': 'User Detail Page',
        'text': '{0}'.format(user),
        'li_set': (
            'Username: "{0}"'.format(user.username),
            'First Name: "{0}"'.format(user.first_name),
            'Last Name: "{0}"'.format(user.last_name),
            'Is Active: "{0}"'.format(user.is_active),
            'Is SuperUser: "{0}"'.format(user.is_superuser),
            'Is Staff: "{0}"'.format(user.is_staff),
        )
    })


def redirect_to_index(request):
    """"""
    return redirect('expanded_test_cases:index')
