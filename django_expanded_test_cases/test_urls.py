"""
Testing URL configuration for django-expanded-test-cases project.

Mocks being an "app" urls.py file.
"""

# Third-Party Imports.
from django.urls import path

# Internal Imports.
from . import test_views


app_name = 'django_expanded_test_cases'
urlpatterns = [
    # Simple test views.
    path('home/', test_views.home, name='home'),
    path('login/', test_views.login, name='login'),
    path('views/one-message/', test_views.view_with_one_message, name='response-with-one-message'),
    path('views/two-messages/', test_views.view_with_two_messages, name='response-with-two-messages'),
    path('views/three-messages/', test_views.view_with_three_messages, name='response-with-three-messages'),
    path('views/repeating-elements/', test_views.view_with_repeating_elements, name='response-with-repeating-elements'),
    path('views/<int:id>/<str:name>/', test_views.view_with_args, name='response-with-args'),
    # Template response views.
    path('template-response/home/', test_views.template_response_home, name='template-response-home'),
    path(
        'template-response/messages/',
        test_views.template_response_with_three_messages,
        name='template-response-messages',
    ),
    path(
        'template-response/<int:id>/<str:name>/',
        test_views.template_response_with_args,
        name='template-response-with-args',
    ),
    # Json response views.
    path('json/index/', test_views.json_response_index, name='json-response-index'),
    # Model test views.
    path('user/detail/<int:pk>/', test_views.user_detail, name='user-detail'),
    # Redirect views.
    path('redirect/index/', test_views.redirect_to_index, name='redirect-to-index'),
    path('redirect/with_args/<int:id>/<str:name>/', test_views.redirect_with_args, name='redirect-with-args'),
    # Form views.
    path('forms/basic-form/', test_views.view_with_basic_form, name='response-with-basic-form'),
    path('forms/basic-formset/', test_views.view_with_basic_formset, name='response-with-basic-formset'),
    path('forms/alt-form/', test_views.view_with_alt_form_name, name='response-with-alt-form-name'),
    path('forms/alt-formset/', test_views.view_with_alt_formset_name, name='response-with-alt-formset-name'),
    # Index view.
    path('', test_views.index, name='index'),
]
