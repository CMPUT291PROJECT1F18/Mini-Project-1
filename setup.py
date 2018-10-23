#!/usr/bin/python
# -*- coding: utf-8 -*-

"""setup.py for mini-project-1"""

import codecs
import re
import sys
import os

from setuptools import setup, find_packages
from setuptools.command.test import test


def find_version(*file_paths):
    with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), *file_paths), "r") as fp:
        version_file = fp.read()
    m = re.search(r"^__version__ = \((\d+), ?(\d+), ?(\d+)\)", version_file, re.M)
    if m:
        return "{}.{}.{}".format(*m.groups())
    raise RuntimeError("Unable to find a valid version")


VERSION = find_version("mini_project_1", "__init__.py")


class Pylint(test):
    def run_tests(self):
        from pylint.lint import Run
        Run(["mini_project_1", "--persistent", "y", "--rcfile", ".pylintrc"])


class PyTest(test):
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        test.initialize_options(self)
        self.pytest_args = "-v --cov={}".format("mini_project_1")

    def run_tests(self):
        import shlex
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


setup(
    name="mini-project-1",
    version=VERSION,
    description="",
    long_description=open("README.rst").read(),
    keywords="",
    author="Nathan Klapstein",
    author_email="nklapste@ualberta.ca",
    url="https://github.com/CMPUT291PROJECT1F18/Mini-Project-1",
    license="MIT License",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    tests_require=[
        "pytest",
        "pytest-cov",
        "pytest-timeout",
        "pylint>=1.9.1,<2.0.0",
        "tox>=3.5.2"
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    cmdclass={"test": PyTest, "lint": Pylint},
)
