"""
Testing views for django-expanded-test-cases project.
"""

# Third-Party Imports.
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.template.response import TemplateResponse


def index(request):
    """Page that simulates a site index/home."""

    # Render response.
    return render(request, 'django_expanded_test_cases/index.html', {
        'header': 'Home Page',
        'text': 'Pretend this is the project landing page.',
    })


def template_response_index(request):
    """Page that simulates a site index/home. Specifically served as TemplateResponse."""

    # Render response.
    return TemplateResponse(request, 'django_expanded_test_cases/index.html', {
        'header': 'Home Page',
        'text': 'Pretend this is the project landing page.',
    })


def login(request):
    """Page that simulates a login page."""

    # Render response.
    return render(request, 'django_expanded_test_cases/index.html', {
        'header': 'Login Page',
        'text': 'Pretend this is a login page.',
    })


def view_with_one_message(request):
    """Page that simulates a view with a single message."""

    # Generate response messages.
    messages.info(request, 'This is a test message.')

    # Render response.
    return render(request, 'django_expanded_test_cases/index.html', {
        'header': 'View with One Message',
        'text': (
            'Pretend useful stuff is displayed here, for one-message render() view.'
        )
    })


def view_with_two_messages(request):
    """Page that simulates a view with two messages."""

    # Generate response messages.
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
    """Page that simulates a view with three messages."""

    # Generate response messages.
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


def view_with_repeating_elements(request):
    """Page that simulates a view with multiple repeating elements."""

    # Render response.
    return render(request, 'django_expanded_test_cases/index.html', {
        'header': 'View with Repeating Elements',
        'text': (
            'Pretend useful stuff is displayed here, for render() view with url args.'
        ),
        'li_set': (
            '<p>Repeating Line</p>',
            '<p>Test First Unique Line</p>',
            '<p>Repeating Line</p>',
            '<p>Test Second Unique Line</p>',
            '<p>Repeating Line</p>',
            '<p>Test Third Unique Line</p>',
            '<p>Repeating Line</p>',
        ),
    })


def view_with_args(request, id, name):
    """Page that simulates a view with passed args."""

    # Render response.
    return render(request, 'django_expanded_test_cases/index.html', {
        'header': 'View with Args',
        'text': (
            'Pretend useful stuff is displayed here, for render() view with url args.'
        ),
        'li_set': (
            'id: "{0}"'.format(id),
            'name: "{0}"'.format(name),
        ),
    })


def template_response_with_three_messages(request):
    """Page that simulates a view with three messages. Specifically served as TemplateResponse."""

    # Generate response messages.
    messages.info(request, 'Test info message.')
    messages.warning(request, 'Test warning message.')
    messages.error(request, 'Test error message.')

    # Render response.
    return TemplateResponse(request, 'django_expanded_test_cases/index.html', {
        'header': 'TemplateResponse View with Three Messages',
        'text': (
            'Pretend useful stuff is displayed here, for three-message TemplateResponse view.'
        )
    })


def template_response_with_args(request, id, name):
    """Page that simulates a view with passed args. Specifically served as a TemplateResponse."""

    # Render response.
    return TemplateResponse(request, 'django_expanded_test_cases/index.html', {
        'header': 'TemplateResponse View with Args',
        'text': (
            'Pretend useful stuff is displayed here, for TemplateResponse view with url args.'
        ),
        'li_set': (
            'id: "{0}"'.format(id),
            'name: "{0}"'.format(name),
        ),
    })


def user_detail(request, pk):
    """Page that simulates a model detail page."""

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
    """Page that simulates a redirect."""

    # Redirect to intended view.
    return redirect('django_expanded_test_cases:index')


def redirect_with_args(request, id, name):
    """Page that simulates a redirect, with included url args."""

    # Redirect to intended view.
    return redirect(reverse(
        'django_expanded_test_cases:template-response-with-args',
        args=(id, name),
    ))
