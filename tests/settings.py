"""
Settings for django-expanded-test-cases UnitTesting.
"""

import sys


SECRET_KEY = 'test-secret-key'


INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'tests.apps.DjangoExpandedTestCasesConfig',
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


TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
}]


# Suppress or show testcase debug printout, based on UnitTest execution method.
if 'pytest' in sys.modules:
    # Running Pytest env.
    # Pytest only shows console output on test failure, so we want it on.
    DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT = True
else:
    # Running other testing env (mostly likely "django manage.py test").
    # manage.py shows all console output always, even on success.
    # So we want it off to avoid information overload and spam.
    DJANGO_EXPANDED_TESTCASES_DEBUG_PRINT = False
