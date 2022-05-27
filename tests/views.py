"""
Testing views for django-expanded-test-cases project.
"""

# System Imports.
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from django.template.response import TemplateResponse


def index(request):
    """"""
    # Render response.
    return render(request, 'django_expanded_test_cases/index.html', {
        'header': 'Home Page',
        'text': 'Pretend this the project landing page.',
    })


def template_response_index(request):
    """"""
    # Render response.
    return render(request, 'django_expanded_test_cases/index.html', {
        'header': 'Home Page',
        'text': 'Pretend this the project landing page.',
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
            'Pretend the message is displayed here. It still shows up in context var though, '
            'which is what we care about for verifying TextCase functionality.'
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
            'Pretend the messages are displayed here. They still show up in context var though, '
            'which is what we care about for verifying TextCase functionality.'
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
            'Pretend the messages are displayed here. They still show up in context var though, '
            'which is what we care about for verifying TextCase functionality.'
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
            'Pretend the messages are displayed here. They still show up in context var though, '
            'which is what we care about for verifying TextCase functionality.'
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
    })

