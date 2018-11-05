#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Search for rides

The member should be able to enter 1-3 location keywords and retrieve all
rides that match all keywords. A ride matches a keyword if the keyword
matches one of the locations source, destination, or enroute. Also a
location matches a keyword if the keyword is either the location code or a
substring of the city, the province, or the address fields of the location.
For each matching ride, all information about the ride (from the rides
table) and car details (if any) will be displayed. If there are more than 5
matches, at most 5 will be shown at a time, and the member is provided an
option to see more. The member should be able to select a ride and message
the member posting the ride that h/she wants to book seats on that ride.
"""

from mini_project_1.common import ShellArgumentParser


def get_search_for_ride_parser() -> ShellArgumentParser:
    """Argparser for the :class:`.shell.MiniProjectShell`
    ``search_rides`` command"""
    parser = ShellArgumentParser(
        prog="search_rides",
        add_help=False,
        description="Search for a ride and if one is selected sent a message "
                    "of intent to join")

    parser.add_argument("term1",
                        help="Location search term to use to look rides")
    parser.add_argument("term2", nargs='?', default=None,
                        help="Location search term to use to look rides")
    parser.add_argument("term3", nargs='?', default=None,
                        help="Location search term to use to look rides")
    return parser
