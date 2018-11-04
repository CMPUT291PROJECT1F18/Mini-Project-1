#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Main command shell for mini-project-1"""

import argparse
import sys
import cmd
import sqlite3
from getpass import getpass
from logging import getLogger
from mini_project_1.loginsession import LoginSession

__log__ = getLogger(__name__)


# TODO: maybe have a try catch structure for all commands invocation
class MiniProjectShell(cmd.Cmd):
    """Main shell for mini-project-1"""
    intro = \
        "Welcome to mini-project-1 shell. Type help or ? to list commands\n"
    prompt = "mini-project-1>"
    login_session: LoginSession = None

    def __init__(self, database: sqlite3.Connection):
        """Initialize the mini-project-1 shell

        :param database: :class:`sqlite3.Connection` to the database to
        interact with the mini-project-1 shell
        """
        super().__init__()
        self.database = database

    # ===============================
    # Shell command definitions
    # ===============================

    def do_login(self, arg):
        """Login to the mini-project-1 database: login"""
        username = str(input("username: "))
        password = getpass("password: ")
        self.login(username, password)

    def do_logout(self, arg):
        """Logout to the mini-project-1 database: logout"""
        self.logout()

    def do_exit(self, arg):
        """Logout (if needed) and exit out of the mini-project-1 shell: exit"""
        if self.login_session:
            self.logout()
        __log__.info("exiting mini-project-1 shell")
        self.database.close()
        return True

    def do_offer_ride(self, arg):
        """Offer a ride"""
        # TODO:

    def do_search_rides(self, arg):
        """Search for ride"""
        # TODO:

    def do_list_bookings(self, arg):
        """List all of your bookings you offer"""
        # TODO:

    def do_book_member(self, arg):
        """Book other members on a ride"""
        # TODO:

    def do_cancel_booking(self, arg):
        """Cancel a booking"""
        cur = self.database.cursor()
        parser = get_cancel_booking_parser()
        try:
            args = parser.parse_args(arg.split())
            delete_booking = 'DELETE FROM bookings WHERE bno=? AND email=?'
            cur.execute(delete_booking, (args.bno, self.login_session.username,))
            # TODO: Spit out messages for ineffective commands
            # TODO: e.g. User has no rides, bno and email mismatch, etc.
        except ShellArgumentException as e:
            print(e)

    def help_cancel_bookings(self):
        """Cancel a booking"""
        parser = get_cancel_booking_parser()
        parser.print_help()

    def do_post_ride_request(self, arg):
        """Post a ride request"""
        # TODO:

    def do_list_ride_requests(self, arg):
        """List all of your ride requests"""
        # TODO:

    def do_search_ride_requests(self, arg):
        """Search for a ride request"""
        # TODO:

    def do_delete_ride_request(self, arg):
        """Delete a ride request"""
        # TODO:

    # ===============================
    # Shell functionality definitions
    # ===============================

    def logout(self):
        """Logout method"""
        if self.login_session:
            email = self.login_session.email
            self.login_session = None
            __log__.info("logging out user: {}".format(email))
        else:
            # TODO: possibly through error instead
            __log__.error("cannot logout not logged in")

    def login(self, email: str, password: str):
        """Login method"""
        if self.login_session:
            __log__.error("already logged in as user: {}".format(self.login_session.email))
        else:
            user_hit = self.database.execute("select email, pwd from members where email = ? and pwd = ?",
                                             (email.lower(), password)).fetchone()
            if user_hit:
                self.login_session = LoginSession(user_hit[0], user_hit[1])
                __log__.info("logged in user: {}".format(user_hit[0]))
            else:
                __log__.warning("invalid login: bad username/password")


def parse(arg):
    """Convert a series of zero or more numbers to an argument tuple"""
    return tuple(arg.split())


class ShellArgumentException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class ShellArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help(sys.stderr)
        raise ShellArgumentException(message)


def get_cancel_booking_parser():
    parser = ShellArgumentParser(
        add_help=False,
        description="Test")

    parser.add_argument("bno", type=int, help="The booking identification number")
    return parser
