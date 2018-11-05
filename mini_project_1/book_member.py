#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Book members

The member should be able to book other members on the rides they offer. 

The member should be able to select a ride and book a member for that ride
by entering the member email, the number of seats booked, the cost per seat,
and pickup and drop off location codes.

Your system should assign a unique booking number (bno) to the booking. 

Your system should give a warning if a ride is being 
overbooked (i.e. the number of seats booked exceeds the number of seats 
offered), but will allow overbooking if the member confirms it. 

After a successful booking, a proper message should be sent to the other
member that s/he is booked on the ride.
"""

import sqlite3

from mini_project_1.common import ShellArgumentParser, \
    greater_than_zero_number, price


def get_book_member_parser() -> ShellArgumentParser:
    """Argparser for the :class:`.shell.MiniProjectShell`
    ``book_member`` command"""
    parser = ShellArgumentParser(
        prog="book_member",
        add_help=False,
        description="Book a member on a ride")

    parser.add_argument("email",
                        help="Email of the member who will be booked on "
                             "the ride")
    parser.add_argument("seats", type=greater_than_zero_number,
                        help="The number of seats booked")
    parser.add_argument("price", type=price,
                        help="The cost per seat for the ride")
    parser.add_argument("pickup",
                        help="Keyword for the pickup location of the ride")
    parser.add_argument("dropoff",
                        help="Keyword for the dropoff location of the ride")
    return parser


def book_member(database: sqlite3.Connection, rno: int, email: str, seats: int,
                seat_price: int, src: str, dst: str):
    """Books a member on a ride and generates its booking number"""
    dbcursor = database.cursor()
    dbcursor.execute("Select MAX(bno) from bookings")
    bno = int(dbcursor.fetchone()[0]) + 1
    try:
        dbcursor.execute("INSERT into Bookings values(?,?,?,?,?,?,?)", (bno, email, rno, seat_price, seats, src, dst))
        database.commit()
        print("Booking added")
    except sqlite3.InterfaceError:
        return False
    return True
