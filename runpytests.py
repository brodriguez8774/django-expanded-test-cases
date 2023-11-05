#!/usr/bin/env python
"""Run Pytest Tests"""

# System Imports.
import os
import subprocess
import sys


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def runtests():
    """Run Tests"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
    os.environ.setdefault('PYTHONPATH', ROOT_DIR)

    # os.environ.setdefault('EXPANDED_TEST_CASES_SELENIUM_BROWSER', 'firefox')
    argv = ['pytest'] + sys.argv[1:] + ['--asyncio-mode=auto']
    subprocess.run(argv, check=False)


if __name__ == '__main__':
    runtests()
