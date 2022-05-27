"""
Testing URL configuration for django-expanded-test-cases project.

Mocks being an "app" urls.py file.
"""

# System Imports.
from django.urls import path

# User Imports.
from . import views


app_name = 'expanded_test_cases'
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

    # Index view.
    path('', views.index, name='index'),
]
