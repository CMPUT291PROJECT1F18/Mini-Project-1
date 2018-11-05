#!/usr/bin/python
# -*- coding: utf-8 -*-

"""functionality defining the ``search_ride_request`` requirement

The member should be able to see all his/her ride requests. Also the member
should be able to provide a location code or a city and see a listing of all
requests with a pickup location matching the location code or the city
entered. If there are more than 5 matches, at most 5 matches will be shown
at a time. The member should be able to select a request and message the
posting member, for example asking the member to check out a ride.
"""

from mini_project_1.common import ShellArgumentParser


def get_search_ride_requests_by_location_code_parser() -> ShellArgumentParser:
    parser = ShellArgumentParser(
        add_help=False,
        description="Search ride requests by location code")

    parser.add_argument("lcode", help="The location code to search by")

    return parser


def get_search_ride_requests_by_city_name_parser() -> ShellArgumentParser:
    parser = ShellArgumentParser(
        add_help=False,
        description="Search ride requests by city name")

    parser.add_argument("city", help="The name of the city to search by")

    return parser


def print_5_and_prompt(rows):
    """Print out 5 rows and if more rows exist prompt the user
    if they want more. If the user enters ``all`` print the remaining rows."""
    if len(rows) > 5:
        print("First 5 rows:")
        for row in rows[:5]:
            print(row)
        see_more = input("Enter 'all' to see all results or enter anything "
                         "else to finish.\n").lower()
        if see_more == "all":
            print("All rows:")
            for row in rows:
                print(row)
    else:
        for row in rows:
            print(row)