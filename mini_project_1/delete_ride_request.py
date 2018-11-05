#!/usr/bin/python
# -*- coding: utf-8 -*-

"""functionality defining the ``delete_ride_request`` requirement

The member should be able to delete any of his/her ride requests.
"""

from mini_project_1.common import ShellArgumentParser


def get_delete_ride_request_parser() -> ShellArgumentParser:
    parser = ShellArgumentParser(
        add_help=False,
        description="Delete a ride request by rid")

    parser.add_argument("rid", type=int,
                        help="The ID of the ride request to delete")

    return parser
