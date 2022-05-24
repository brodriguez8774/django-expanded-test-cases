"""
Settings for django-expanded-test-cases UnitTesting.
"""


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


ROOT_URLCONF = 'tests.urls_root'
LOGIN_URL = 'expanded_test_cases:login'
