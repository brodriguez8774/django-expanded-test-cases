"""
Settings for django-expanded-test-cases UnitTesting.
"""

# System Imports.
import os, sys


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'test-secret-key'


# Determine if channels is installed.
try:
    from channels.testing import ChannelsLiveServerTestCase

    # If we made it this far, channels is installed.
    CHANNELS_PACKAGE_INSTALLED = True
except ModuleNotFoundError:
    # Failed to import channels. Assume not installed.
    CHANNELS_PACKAGE_INSTALLED = False


INSTALLED_APPS = (
    'django_expanded_test_cases',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)
if CHANNELS_PACKAGE_INSTALLED:
    INSTALLED_APPS += ('channels', 'daphne')
ASGI_APPLICATION = 'tests.asgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'TEST': {
            'NAME': os.path.join(BASE_DIR, 'db_test.sqlite3'),
        },
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


ROOT_URLCONF = 'tests.urls'
LOGIN_URL = 'django_expanded_test_cases:login'
STATIC_URL = '/static/'
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


# Extra definable package settings.
# Here for personal reference at later point, for documentation and such.
# DJANGO_EXPANDED_TESTCASES_ALLOW_MESSAGE_PARTIALS = True
# DJANGO_EXPANDED_TESTCASES_MATCH_ALL_CONTEXT_MESSAGES = False

# Valid, supported selenium browser options.
# SELENIUM_TEST_BROWSER = 'chrome'
# SELENIUM_TEST_BROWSER = 'chromium'
# SELENIUM_TEST_BROWSER = 'firefox'

# Support for changing console color output.
# from colorama import Back, Fore, Style
# DJANGO_EXPANDED_TESTCASES_OUTPUT_EXPECTED_MATCH = '{0}{1}{2}'.format(Fore.CYAN, Back.RESET, Style.NORMAL)
# DJANGO_EXPANDED_TESTCASES_OUTPUT_EXPECTED_ERROR = '{0}{1}{2}'.format(Fore.BLACK, Back.CYAN, Style.NORMAL)
# DJANGO_EXPANDED_TESTCASES_OUTPUT_ACTUALS_MATCH = '{0}{1}{2}'.format(Fore.MAGENTA, Back.RESET, Style.NORMAL)
# DJANGO_EXPANDED_TESTCASES_OUTPUT_ACTUALS_ERROR = '{0}{1}{2}'.format(Fore.BLACK, Back.MAGENTA, Style.NORMAL)
