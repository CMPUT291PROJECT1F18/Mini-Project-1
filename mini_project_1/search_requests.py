#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Search for a ride request

The member should be able to see all his/her ride requests. Also the member
should be able to provide a location code or a city and see a listing of all
requests with a pickup location matching the location code or the city
entered. If there are more than 5 matches, at most 5 matches will be shown
at a time. The member should be able to select a request and message the
posting member, for example asking the member to check out a ride.
"""

from mini_project_1.common import ShellArgumentParser


def get_search_requests_lcode_parser() -> ShellArgumentParser:
    """Argparser for the :class:`.shell.MiniProjectShell`
    ``search_requests_lcode`` command"""
    parser = ShellArgumentParser(
        prog="search_requests_lcode",
        description="Search ride requests by location code")

    parser.add_argument("lcode", help="The location code to search by")

    return parser


def get_search_requests_city_parser() -> ShellArgumentParser:
    """Argparser for the :class:`.shell.MiniProjectShell`
    ``search_requests_city`` command"""
    parser = ShellArgumentParser(
        prog="search_requests_city",
        description="Search ride requests by city name")

    parser.add_argument("city", help="The name of the city to search by")

    return parser


def print_5_and_prompt(rows):
    """Print out 5 rows and if more rows exist prompt the user
    if they want more. If the user enters ``all`` print the remaining rows."""
    if len(rows) > 5:
        index = 0
        while index < len(rows)-1:
            end_index = min(index + 5, len(rows))
            print("Rows {}-{}:".format(index+1, end_index))
            for row in rows[index:end_index]:
                print(row)
            if end_index == len(rows):
                break
            see_more = input(
                "Enter 'more' to see 5 more results or enter "
                "anything else to finish.\n").lower()
            if see_more != "more":
                break
            else:
                index = index + 5
    else:
        print("All rows:")
        for row in rows:
            print(row)
