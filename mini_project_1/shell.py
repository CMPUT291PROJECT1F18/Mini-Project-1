#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Main command shell for mini-project-1"""

import cmd
import sqlite3
from getpass import getpass
from logging import getLogger

from mini_project_1.ride import offer_ride

from mini_project_1.member import Member

__log__ = getLogger(__name__)


# TODO: maybe have a try catch structure for all commands invocation
class MiniProjectShell(cmd.Cmd):
    """Main shell for mini-project-1"""
    intro = \
        "Welcome to mini-project-1 shell. Type help or ? to list commands\n"
    prompt = "mini-project-1>"
    login_member: Member = None

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
        if self.login_member:
            self.logout()
        __log__.info("exiting mini-project-1 shell")
        self.database.close()
        return True

    def do_offer_ride(self, arg):
        """Offer a ride"""
        # TODO:
        if self.login_member:
            if offer_ride(self.database.cursor(), self.login_member):
                print("Ride added!")
            else:
                print("Did not add a ride...   8-( ")
        else:
            print("Must be logged in to offer a ride.")

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
        # TODO:

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
        if self.login_member:
            username = self.login_member.username
            self.login_member = None
            __log__.info("logging out user: {}".format(username))
        else:
            # TODO: possibly through error instead
            __log__.error("cannot logout not logged in")

    def login(self, username: str, password: str):
        """Login method"""
        # TODO: validate login
        self.login_member = Member(username, password)
        __log__.info("logged in user: {}".format(username))
