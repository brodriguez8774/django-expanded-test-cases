#!/usr/bin/env python
"""Run Package Pytest Tests"""

# System Imports.
import os
import subprocess
import sys


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def runtests():
    """Run tests with pytest format.
    Has very helpful and verbose testing output.
    """

    # Set environment values.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
    os.environ.setdefault('PYTHONPATH', ROOT_DIR)

    # Run tests.
    argv = ['pytest'] + sys.argv[1:]
    proc = subprocess.run(argv, check=False)
    return proc.returncode


if __name__ == '__main__':
    sys.exit(runtests())
