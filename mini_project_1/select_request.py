#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Select a ride request"""

from mini_project_1.common import ShellArgumentParser


def get_select_request_parser() -> ShellArgumentParser:
    """Argparser for the :class:`.shell.MiniProjectShell`
    ``select_request`` command"""
    parser = ShellArgumentParser(
        prog="select_request",
        add_help=False,
        description="Select a ride request and perform actions with it"
    )

    parser.add_argument("rid", type=int,
                        help="The ID of the ride request to delete")

    return parser
