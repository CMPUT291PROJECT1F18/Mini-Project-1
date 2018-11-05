#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Logout functionality"""

from mini_project_1.common import ShellArgumentParser


def get_logout_parser() -> ShellArgumentParser:
    """Argparser for the :class:`.shell.MiniProjectShell` ``logout`` command"""
    parser = ShellArgumentParser(
        prog="logout",
        add_help=False,
        description="Logout to the mini-project-1 database")

    return parser
