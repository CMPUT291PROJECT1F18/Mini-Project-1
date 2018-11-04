#!/usr/bin/python
# -*- coding: utf-8 -*-

"""pytests for :mod:`.__main__`"""

from mini_project_1.__main__ import get_parser, main

import mock


def test_get_parser():
    parser = get_parser()
    assert parser


def test_main(tmpdir):
    tmp_file = tmpdir.join("thefile_name.json")
    tmp_file_name = str(tmp_file)
    with mock.patch('builtins.input', return_value='foo'):
        with mock.patch('mini_project_1.shell.MiniProjectShell.cmdloop', return_value='bar'):
            main(["-i", tmp_file_name])
