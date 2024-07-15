"""
Imports logic for "django_expanded_test_cases/" folder.
Allows simplified importing, for use as a third-party package.
"""

# Import TestCase classes.
from .test_cases import *


"""Version declaration"""

__version__ = "0.7.2"


def parse_version(version):
    """
    '0.1.2.dev1' -> (0, 1, 2, 'dev1')
    '0.1.2' -> (0, 1, 2)
    """
    v = version.split(".")
    ret = []
    for p in v:
        if p.isdigit():
            ret.append(int(p))
        else:
            ret.append(p)
    return tuple(ret)


VERSION = parse_version(__version__)


# Define acceptable imports on file.
__all__ = [
    'BaseTestCase',
    'IntegrationTestCase',
    'LiveServerTestCase',
    'ChannelsLiveServerTestCase',
    'VERSION',
]
