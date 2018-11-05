#!/usr/bin/python
# -*- coding: utf-8 -*-

"""List bookings

The member should be able to list all bookings on rides s/he offers.
"""

from mini_project_1.common import ShellArgumentParser


def get_list_bookings_parser() -> ShellArgumentParser:
    parser = ShellArgumentParser(
        prog="list_bookings",
        add_help=False,
        description="List all the bookings that you offer")

    return parser

