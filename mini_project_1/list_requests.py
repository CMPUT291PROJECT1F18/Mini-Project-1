#!/usr/bin/python
# -*- coding: utf-8 -*-

"""List requests

The member should be able to see all his/her ride requests.
"""

from mini_project_1.common import ShellArgumentParser


def get_list_ride_requests_parser() -> ShellArgumentParser:
    """Argparser for the :class:`.shell.MiniProjectShell`
    ``list_requests`` command"""
    parser = ShellArgumentParser(
        prog="list_requests",
        description="List all the ride requests that you offer")

    return parser

