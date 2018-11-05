#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Offer a ride

The member should be able to offer rides by providing a date, the number of
seats offered, the price per seat, a luggage description, a source location,
and a destination location. The member should have the option of adding a
car number and any set of enroute locations.
"""

import sqlite3

import pendulum

from mini_project_1.common import ShellArgumentParser, date, \
    greater_than_zero_number, price
from mini_project_1.loginsession import LoginSession


def get_offer_ride_parser() -> ShellArgumentParser:
    """Argparser for the :class:`.shell.MiniProjectShell`
    ``offer_ride`` command"""
    parser = ShellArgumentParser(
        prog="offer_ride",
        add_help=False,
        description="Offer a ride")

    # date, seats, price, luggage, source, destination, cno, enroute
    parser.add_argument("date", type=date,
                        help="Date the ride should start on (eg: 1975-05-21T22:00:00)")
    parser.add_argument("seats", type=greater_than_zero_number,
                        help="The number of seats offered")
    parser.add_argument("price", type=price,
                        help="The amount you want per seat for the ride")
    parser.add_argument("luggage",
                        help="Description of car luggage")
    parser.add_argument("src",
                        help="Keyword for the start location of the ride")
    parser.add_argument("dst",
                        help="Keyword for the end location of the ride")
    parser.add_argument("--cno", nargs='?', default=None,
                        help="Your car number to use")
    parser.add_argument("--enroute", nargs='+', default=set(),
                        help="Enroute locations to go to")
    return parser


def offer_ride(database: sqlite3.Connection, member: LoginSession, date: pendulum.DateTime,
               seats: int, price: int, luggage: str, source: str, destination: str,
               cno: str = None, enroute: set = set()):
    """
    Tries to add a ride to the database for the member
    :return: if a ride has been added (True/False)
    """
    dbcursor = database.cursor()
    dbcursor.execute(
        "SELECT MAX(rno) "
        "FROM rides"
    )
    rno = str(int(dbcursor.fetchone()[0]) + 1)

    try:
        dbcursor.execute(
            "INSERT INTO rides (rno, price, rdate, seats, lugDesc, src, dst, driver) VALUES " +
            "(?, ?, ?, ?, ?, ?, ?, ?)",
            (rno, price, date, seats, luggage, source, destination, member.get_email())
        )

        if cno:
            dbcursor.execute(
                "UPDATE rides "
                "SET cno = ? "
                "WHERE rno = ?",
                (cno, rno)
            )

        for place in enroute:
            dbcursor.execute(
                "INSERT INTO enroute (rno, lcode) VALUES (?, ?)",
                (rno, place)
            )
    except sqlite3.OperationalError as e:
        print(e)
        return False
    except sqlite3.IntegrityError as e:
        print(e)
        return False

    database.commit()
    return True


def check_valid_cno(dbcursor: sqlite3.Cursor, cno: int, member: LoginSession):
    """Returns whether a member has a car number cno in the database with
    cursor dbcursor"""
    dbcursor.execute(
        "SELECT cno "
        "FROM cars "
        "WHERE cno = ? AND owner = ?",
        (cno, member.get_email())
    )
    if dbcursor.fetchall():
        return True
    return False
