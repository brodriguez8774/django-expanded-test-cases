"""
URL configuration for django-expanded-test-cases project UnitTests.

Mocks being an "app" urls.py file.
"""

# Third-Party Imports.
from django.urls import path

# Internal Imports.
from tests.django_expanded_test_cases.testing import views


app_name = 'django_expanded_test_cases'
urlpatterns = [
    # Simple test views.
    path('home/', views.home, name='home'),
    path('home-no-slash', views.home, name='home-no-trailing-slash'),
    path('login/', views.login, name='login'),
    path('views/one-message/', views.view_with_one_message, name='response-with-one-message'),
    path('views/two-messages/', views.view_with_two_messages, name='response-with-two-messages'),
    path('views/three-messages/', views.view_with_three_messages, name='response-with-three-messages'),
    path('views/repeating-elements/', views.view_with_repeating_elements, name='response-with-repeating-elements'),
    path('views/<int:id>/<str:name>/', views.view_with_args, name='response-with-args'),
    # Template response views.
    path('template-response/home/', views.template_response_home, name='template-response-home'),
    path(
        'template-response/messages/',
        views.template_response_with_three_messages,
        name='template-response-messages',
    ),
    path(
        'template-response/<int:id>/<str:name>/',
        views.template_response_with_args,
        name='template-response-with-args',
    ),
    # Json response views.
    path('json/basic-dict/', views.json_response_basic_dict, name='json-response-basic-dict'),
    path('json/basic-list/', views.json_response_basic_list, name='json-response-basic-list'),
    # Model test views.
    path('user/detail/<int:pk>/', views.user_detail, name='user-detail'),
    # Redirect views.
    path('redirect/index/', views.redirect_to_index, name='redirect-to-index'),
    path('redirect/one-message/', views.redirect_to_one_message, name='redirect-to-one-message'),
    path('redirect/basic-form/', views.redirect_to_basic_form, name='redirect-to-basic-form'),
    path('redirect/with_args/<int:id>/<str:name>/', views.redirect_with_args, name='redirect-with-args'),
    # Form views.
    path('forms/basic-form/', views.view_with_basic_form, name='response-with-basic-form'),
    path('forms/basic-formset/', views.view_with_basic_formset, name='response-with-basic-formset'),
    path('forms/alt-form/', views.view_with_alt_form_name, name='response-with-alt-form-name'),
    path('forms/alt-formset/', views.view_with_alt_formset_name, name='response-with-alt-formset-name'),
    # Index view.
    path('', views.index, name='index'),
]
