"""
Views for django-expanded-test-cases project UnitTests.
"""

# Third-Party Imports.
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from django.urls import reverse

# Internal Imports.
from tests.django_expanded_test_cases.testing.forms import BasicForm, BasicFormset


def index(request):
    """Page that simulates a site index/home."""

    # Render response.
    return render(
        request,
        'django_expanded_test_cases/index.html',
        {
            'header': 'Index Page',
            'text': (
                'Links to various testing pages for the ExpandedTestCases (Etc) package.'
                '<ul>'
                '  <li><a href="' + reverse('django_expanded_test_cases:home') + '">Home Page</a></li>'
                '  <li><a href="' + reverse('django_expanded_test_cases:login') + '">Login Page</a></li>'
                '<br>'
                '  <li><a href="'
                + reverse('django_expanded_test_cases:response-with-one-message')
                + '">One-Message Page</a></li>'
                '  <li><a href="'
                + reverse('django_expanded_test_cases:response-with-two-messages')
                + '">Two-Messages Page</a></li>'
                '  <li><a href="'
                + reverse('django_expanded_test_cases:response-with-three-messages')
                + '">Three-Messages Page</a></li>'
                '  <li><a href="'
                + reverse('django_expanded_test_cases:response-with-repeating-elements')
                + '">Repeating Elements Page</a></li>'
                '  <li><a href="'
                + reverse('django_expanded_test_cases:response-with-args', args=(5, "Test Name"))
                + '">Response with Args</a></li>'
                '<br>'
                '  <li><a href="'
                + reverse('django_expanded_test_cases:json-response-index')
                + '">Json Response</a></li>'
                '<br>'
                '  <li><a href="'
                + reverse('django_expanded_test_cases:user-detail', kwargs={'pk': 1})
                + '">Model Detail Page</a></li>'
                '<br>'
                '  <li><a href="'
                + reverse('django_expanded_test_cases:redirect-to-index')
                + '">Redirect to Index</a></li>'
                '  <li><a href="'
                + reverse('django_expanded_test_cases:redirect-with-args', args=(5, "Test Name"))
                + '">Redirect with Args</a></li>'
                '<br>'
                '  <li><a href="'
                + reverse('django_expanded_test_cases:response-with-basic-form')
                + '">Basic Form</a></li>'
                '  <li><a href="'
                + reverse('django_expanded_test_cases:response-with-basic-formset')
                + '">Basic Formset</a></li>'
                '  <li><a href="'
                + reverse('django_expanded_test_cases:response-with-alt-form-name')
                + '">Alternate Form Name</a></li>'
                '  <li><a href="'
                + reverse('django_expanded_test_cases:response-with-alt-formset-name')
                + '">Alternate Formset Name</a></li>'
                '</ul>'
            ),
        },
    )


def home(request):
    """Page that simulates a site home page."""

    # Render response.
    return render(
        request,
        'django_expanded_test_cases/index.html',
        {
            'header': 'Home Page',
            'text': 'Pretend this is the project landing page.',
        },
    )


def template_response_home(request):
    """Page that simulates a site home page. Specifically served as TemplateResponse."""

    # Render response.
    return TemplateResponse(
        request,
        'django_expanded_test_cases/index.html',
        {
            'header': 'Home Page',
            'text': 'Pretend this is the project landing page.',
        },
    )


def login(request):
    """Page that simulates a login page."""

    # Render response.
    return render(
        request,
        'django_expanded_test_cases/index.html',
        {
            'header': 'Login Page',
            'text': 'Pretend this is a login page.',
        },
    )


def view_with_one_message(request):
    """Page that simulates a view with a single message."""

    # Generate response messages.
    messages.info(request, 'This is a test message.')

    # Render response.
    return render(
        request,
        'django_expanded_test_cases/index.html',
        {
            'header': 'View with One Message',
            'text': ('Pretend useful stuff is displayed here, for one-message render() view.'),
        },
    )


def view_with_two_messages(request):
    """Page that simulates a view with two messages."""

    # Generate response messages.
    messages.info(request, 'Test message #1.')
    messages.warning(request, 'Test message #2.')

    # Render response.
    return render(
        request,
        'django_expanded_test_cases/index.html',
        {
            'header': 'View with Two Messages',
            'text': ('Pretend useful stuff is displayed here, for two-message render() view.'),
        },
    )


def view_with_three_messages(request):
    """Page that simulates a view with three messages."""

    # Generate response messages.
    messages.info(request, 'Test info message.')
    messages.warning(request, 'Test warning message.')
    messages.error(request, 'Test error message.')

    # Render response.
    return render(
        request,
        'django_expanded_test_cases/index.html',
        {
            'header': 'View with Three Messages',
            'text': ('Pretend useful stuff is displayed here, for three-message render() view.'),
        },
    )


def view_with_repeating_elements(request):
    """Page that simulates a view with multiple repeating elements."""

    # Render response.
    return render(
        request,
        'django_expanded_test_cases/index.html',
        {
            'header': 'View with Repeating Elements',
            'text': ('Pretend useful stuff is displayed here, for render() view with url args.'),
            'li_set': (
                '<p>Repeating Line</p>',
                '<p>Test First Unique Line</p>',
                '<p>Repeating Line</p>',
                '<p>Test Second Unique Line</p>',
                '<p>Repeating Line</p>',
                '<p>Test Third Unique Line</p>',
                '<p>Repeating Line</p>',
            ),
        },
    )


def view_with_args(request, id, name):
    """Page that simulates a view with passed args."""

    # Render response.
    return render(
        request,
        'django_expanded_test_cases/index.html',
        {
            'header': 'View with Args',
            'text': ('Pretend useful stuff is displayed here, for render() view with url args.'),
            'li_set': (
                'id: "{0}"'.format(id),
                'name: "{0}"'.format(name),
            ),
        },
    )


def template_response_with_three_messages(request):
    """Page that simulates a view with three messages. Specifically served as TemplateResponse."""

    # Generate response messages.
    messages.info(request, 'Test info message.')
    messages.warning(request, 'Test warning message.')
    messages.error(request, 'Test error message.')

    # Render response.
    return TemplateResponse(
        request,
        'django_expanded_test_cases/index.html',
        {
            'header': 'TemplateResponse View with Three Messages',
            'text': ('Pretend useful stuff is displayed here, for three-message TemplateResponse view.'),
        },
    )


def template_response_with_args(request, id, name):
    """Page that simulates a view with passed args. Specifically served as a TemplateResponse."""

    # Render response.
    return TemplateResponse(
        request,
        'django_expanded_test_cases/index.html',
        {
            'header': 'TemplateResponse View with Args',
            'text': ('Pretend useful stuff is displayed here, for TemplateResponse view with url args.'),
            'li_set': (
                'id: "{0}"'.format(id),
                'name: "{0}"'.format(name),
            ),
        },
    )


def json_response_index(request):
    request_headers = dict(request.headers)
    return JsonResponse(
        {
            'success': 'This is a test Json response.',
            'request_headers': request_headers,
        }
    )


def user_detail(request, pk):
    """Page that simulates a model detail page."""

    # Pull database info.
    user = get_object_or_404(get_user_model(), pk=pk)

    # Render response.
    return render(
        request,
        'django_expanded_test_cases/index.html',
        {
            'header': 'User Detail Page',
            'text': '{0}'.format(user),
            'li_set': (
                'Username: "{0}"'.format(user.username),
                'First Name: "{0}"'.format(user.first_name),
                'Last Name: "{0}"'.format(user.last_name),
                'Is Active: "{0}"'.format(user.is_active),
                'Is SuperUser: "{0}"'.format(user.is_superuser),
                'Is Staff: "{0}"'.format(user.is_staff),
            ),
        },
    )


def redirect_to_index(request):
    """Page that simulates a redirect."""

    # Generate response messages.
    messages.info(request, 'Redirecting to index.')

    # Redirect to intended view.
    return redirect('django_expanded_test_cases:index')


def redirect_to_one_message(request):
    """Page that simulates a redirect."""

    # Generate response messages.
    messages.info(request, 'Redirecting to one-message view.')

    # Redirect to intended view.
    return redirect('django_expanded_test_cases:response-with-one-message')


def redirect_to_basic_form(request):
    """Page that simulates a redirect."""

    # Generate response messages.
    messages.info(request, 'Redirecting to basic form view.')

    # Redirect to intended view.
    return redirect('django_expanded_test_cases:response-with-basic-form')


def redirect_with_args(request, id, name):
    """Page that simulates a redirect, with included url args."""

    # Redirect to intended view.
    return redirect(
        reverse(
            'django_expanded_test_cases:template-response-with-args',
            args=(id, name),
        )
    )


def view_with_basic_form(request):
    """View that simulates a form page."""

    # Get initial form data.
    form = BasicForm()

    # Handle if POST.
    if request.POST:
        form = BasicForm(request.POST)

        # Handle form validation.
        if form.is_valid():
            messages.info(request, 'Form submitted successfully.')

            # Optional logic to simulate resetting a form prior to page render.
            reset_form_on_success = request.POST.get('reset_form_on_success', False)
            if reset_form_on_success:
                # Reset form data.
                form = BasicForm()

    # Render response.
    return render(
        request,
        'django_expanded_test_cases/form.html',
        {
            'header': 'Basic Form Page',
            'form': form,
        },
    )


def view_with_basic_formset(request):
    """View that simulates a formset page."""

    # Get initial form data.
    formset = BasicFormset()

    # Handle if POST.
    if request.POST:
        formset = BasicFormset(request.POST)

        # Handle form validation.
        if formset.is_valid():

            messages.info(request, 'Formset submitted successfully.')

            # Optional logic to simulate resetting a form prior to page render.
            reset_form_on_success = request.POST.get('reset_form_on_success', False)
            if reset_form_on_success:
                # Reset form data.
                formset = BasicFormset()

    # Render response.
    return render(
        request,
        'django_expanded_test_cases/form.html',
        {
            'header': 'Basic Formset Page',
            'formset': formset,
        },
    )


def view_with_alt_form_name(request):
    """View that simulates a form page using a different name."""

    # Get initial form data.
    form = BasicForm()

    # Handle if POST.
    if request.POST:
        form = BasicForm(request.POST)

        # Handle form validation.
        if form.is_valid():
            messages.info(request, 'Form submitted successfully.')

            # Optional logic to simulate resetting a form prior to page render.
            reset_form_on_success = request.POST.get('reset_form_on_success', False)
            if reset_form_on_success:
                # Reset form data.
                form = BasicForm()

    # Render response.
    return render(
        request,
        'django_expanded_test_cases/form_alt.html',
        {
            'header': 'Alt Form Name Page',
            'my_alt_form': form,
        },
    )


def view_with_alt_formset_name(request):
    """View that simulates a formset page."""

    collide_with_manager_form = False

    # Get initial form data.
    formset = BasicFormset()

    # Handle if POST.
    if request.POST:
        formset = BasicFormset(request.POST)
        collide_with_manager_form = request.POST.get('collide_with_manager_form', False)

        # Handle form validation.
        if formset.is_valid():

            messages.info(request, 'Formset submitted successfully.')

            # Optional logic to simulate resetting a form prior to page render.
            reset_form_on_success = request.POST.get('reset_form_on_success', False)
            if reset_form_on_success:
                # Reset form data.
                formset = BasicFormset()

    context = {
        'header': 'Alt Formset Name Page',
        'my_alt_formset': formset,
    }
    if collide_with_manager_form:
        context['form'] = ''

    # Render response.
    return render(
        request,
        'django_expanded_test_cases/form_alt.html',
        context,
    )
