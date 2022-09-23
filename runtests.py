#!/usr/bin/env python
"""Run Pytest Tests"""

# System Imports.
import os
import sys

# Third-Party Imports.
from django.core.management import execute_from_command_line


def runtests():
    """Run Tests"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
    argv = sys.argv[:1] + ['test'] + sys.argv[1:]
    execute_from_command_line(argv)


if __name__ == '__main__':
    runtests()
