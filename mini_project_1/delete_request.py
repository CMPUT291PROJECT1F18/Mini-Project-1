#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Delete a ride request

The member should be able to delete any of his/her ride requests.
"""

from mini_project_1.common import ShellArgumentParser


def get_delete_request_parser() -> ShellArgumentParser:
    """Argparser for the :class:`.shell.MiniProjectShell`
    ``delete_request`` command"""
    parser = ShellArgumentParser(
        prog="delete_request",
        description="Delete a ride request by rid")

    parser.add_argument("rid", type=int,
                        help="The ID of the ride request to delete")

    return parser
