"""
Testing URL configuration for django-expanded-test-cases project.

Mocks being an "app" urls.py file.
"""

# Third-Party Imports.
from django.urls import path

# Internal Imports.
from tests import views


app_name = 'django_expanded_test_cases'
urlpatterns = [
    # Simple test views.
    path('login/', views.login, name='login'),
    path('one-message/', views.view_with_one_message, name='one-message'),
    path('two-messages/', views.view_with_two_messages, name='two-messages'),
    path('three-messages/', views.view_with_three_messages, name='three-messages'),

    # Template response views.
    path('template-response/index/', views.template_response_index, name='template-response-index'),
    path('template-response/messages/', views.template_response_with_three_messages, name='template-response-messages'),

    # Model test views.
    path('user/detail/<int:pk>/', views.user_detail, name='user-detail'),

    # Redirect views.
    path('redirect/index/', views.redirect_to_index, name='redirect-to-index'),

    # Index view.
    path('', views.index, name='index'),
]
