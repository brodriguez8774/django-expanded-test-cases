"""
Imports logic for "django_expanded_test_cases/" folder.
Allows simplified importing, for use as a third-party package.
"""

# Import TestCase classes.
try:
    from .test_cases import *
except:
    # Docs need to access this file to get project version.
    # But this import statement fails on docs build.
    # In that case, it's fine, ignore.
    pass


"""Version declaration"""

__version__ = "0.8.0"


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
    '__version__',
]
