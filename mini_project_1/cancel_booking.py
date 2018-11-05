#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Cancel a booking

The member should be able to cancel any booking on rides s/he offers.
For any booking that is cancelled (i.e. being deleted from the booking table),
a proper message should be sent to the member whose booking is cancelled.
"""

from mini_project_1.common import ShellArgumentParser


def get_cancel_booking_parser() -> ShellArgumentParser:
    """Get a :class:`ShellArgumentParser` for use in parsing the arguments
    for a ``cancel_booking`` command"""
    parser = ShellArgumentParser(
        add_help=False,
        description="Cancel a booking")

    parser.add_argument("bno", type=int,
                        help="The booking identification number")
    return parser
