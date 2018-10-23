#!/usr/bin/python
# -*- coding: utf-8 -*-

"""pytests for :mod:`__main__`"""

from mini_project_1.__main__ import get_parser, main

import pytest


def test_get_parser():
    parser = get_parser()
    assert parser
