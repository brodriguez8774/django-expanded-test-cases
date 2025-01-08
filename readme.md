# Django Expanded Test Cases


[![PyPI](https://img.shields.io/pypi/v/django-expanded-test-cases?color=blue)](https://img.shields.io/pypi/v/django-expanded-test-cases?color=blue)
[![Python Versions](https://img.shields.io/badge/python-%3E%3D3.6-brightgreen)](https://img.shields.io/badge/python-%3E%3D3.6-brightgreen)
[![Django Versions](https://img.shields.io/badge/django-%3E%3D2.2-brightgreen)](https://img.shields.io/badge/django-%3E%3D2.2-brightgreen)
[![Run Tests](https://github.com/brodriguez8774/django-expanded-test-cases/actions/workflows/test.yaml/badge.svg)](https://github.com/brodriguez8774/django-expanded-test-cases/actions/workflows/test.yaml)
[![Coverage Status](https://coveralls.io/repos/github/brodriguez8774/django-expanded-test-cases/badge.svg?branch=main)](https://coveralls.io/github/brodriguez8774/django-expanded-test-cases?branch=main)
[![Documentation Status](https://readthedocs.org/projects/django-expanded-test-cases/badge/?version=latest)](https://django-expanded-test-cases.readthedocs.io/en/latest/?badge=latest)
[![GitHub](https://img.shields.io/github/license/brodriguez8774/django-expanded-test-cases)](https://img.shields.io/github/license/brodriguez8774/django-expanded-test-cases)
[![PyPI Downloads per Month](https://img.shields.io/pypi/dm/django-expanded-test-cases.svg)](https://pypi.python.org/pypi/django-expanded-test-cases)


## Description

Expands the existing [Django](https://docs.djangoproject.com/en/dev/)
[TestCase class](https://docs.djangoproject.com/en/dev/topics/testing/overview/) with extra functionality.

Different TestCase classes are provided, each providing separate sets of functionality.


For full documentation, see [ReadTheDocs](https://django-expanded-test-cases.readthedocs.io/en/latest/).
For changes in the latest version, see [ReadTheDocs - Version History](https://django-expanded-test-cases.readthedocs.io/en/latest/version_history.html).


## Example ETC Debug Output on UnitTest Error
A main functionality that **ExpandedTestCases** provides is verbose response debug info on UnitTest errors.<br>
Below is an example of such output, when a test fails while checking the `<h1>` tag for a very simple page.

![ETC Error Debug Output Screenshot](https://user-images.githubusercontent.com/14208531/231304818-fb0dbe31-ead9-4de8-8efe-a3fc858cbddd.png)


## Installation

Install with

    pip install django-expanded-test-cases

For full color output, also install

    pip install colorama

## Package Development & Running Project Tests

As standard for Python development, this project has its own testing to ensure it functions as desired.
After installing dependencies, everything required to run tests are provided in one of two files:
* To run tests via standard django `python manage.py test`, execute the `<project_root>/runtests.py` file.
* To run tests via `pytest`, execute the `<project_root>/runpytests.py` file.
