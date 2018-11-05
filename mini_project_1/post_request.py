#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Post a ride request

Post ride requests. The member should be able to post a ride request
by providing a date, a pick up location code, a drop off location code,
and the amount willing to pay per seat. The request rid is set by your
system to a unique number and the email is set to the email address of
the member.
"""

import argparse
import sqlite3
from logging import getLogger

import pendulum

from mini_project_1.common import ShellArgumentParser, MINI_PROJECT_DATE_FMT


__log__ = getLogger(__name__)


def price(price_string: str) -> int:
    """Argparser type validation function for validating a price for use in
    ``post_ride_request`` command"""
    price = int(price_string)
    if price < 0:
        raise argparse.ArgumentTypeError(
            "invalid price: {} (please choose a non negative price)".format(
                price_string
            )
        )
    return price


def date(date_str: str) -> pendulum.DateTime:
    """Argparser type validation function for validating a date for use
    in ``post_ride_request`` command"""
    parsed_date = pendulum.parse(date_str)
    if parsed_date >= pendulum.today().subtract(days=1):
        return parsed_date
    else:
        raise argparse.ArgumentTypeError(
            "invalid date: {} (please choose a date from today {} forwards)".format(
                date_str, pendulum.today().strftime(MINI_PROJECT_DATE_FMT)
            )
        )


def get_post_request_parser() -> ShellArgumentParser:
    """Argparser for the :class:`.shell.MiniProjectShell`
    ``post_request`` command"""
    parser = ShellArgumentParser(
        prog="post_request",
        description="Post a ride request")

    parser.add_argument("date", type=date,
                        help="Date the ride should start on (eg: 1975-05-21T22:00:00)")
    parser.add_argument("pickup",
                        help="The location code for the pickup location of "
                             "the ride")
    parser.add_argument("dropoff",
                        help="The location code for the dropoff location of "
                             "the ride")
    parser.add_argument("price", type=price,
                        help="The maximum amount you are willing to pay per "
                             "seat for the ride")
    return parser


def valid_location_code(database: sqlite3.Connection,
                        location_code_str: str) -> bool:
    """Validate that a location ode for use in ``post_ride_request``
    command actually exists in locations"""

    locations = database.execute(
        "SELECT lcode "
        "FROM locations "
        "WHERE locations.lcode = ?",
        (location_code_str,)
    ).fetchone()
    if not locations:
        __log__.error("invalid location code: {}".format(location_code_str))
        return False
    else:
        return True
