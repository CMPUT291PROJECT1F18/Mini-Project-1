#!/usr/bin/python
# -*- coding: utf-8 -*-

"""List bookings

The member should be able to list all bookings on rides s/he offers.
"""

from mini_project_1.common import ShellArgumentParser


def get_list_bookings_parser() -> ShellArgumentParser:
    """Argparser for the :class:`.shell.MiniProjectShell`
    ``list_bookings`` command"""
    parser = ShellArgumentParser(
        prog="list_bookings",
        description="List all the bookings that you offer")

    return parser

