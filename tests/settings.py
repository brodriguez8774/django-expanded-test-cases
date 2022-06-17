"""
Settings for django-expanded-test-cases UnitTesting.
"""

import sys


SECRET_KEY = 'test-secret-key'


INSTALLED_APPS = (
    'tests.apps.DjangoExpandedTestCasesConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'tests.urls_root'
LOGIN_URL = 'expanded_test_cases:login'
USE_TZ = True


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Extra definable package settings.
# Here for personal reference at later point, for documentation and such.
# DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT = True
# DJANGO_EXPANDED_TESTCASES_ALLOW_MESSAGE_PARTIALS = True
# DJANGO_EXPANDED_TESTCASES_MATCH_ALL_CONTEXT_MESSAGES = False
