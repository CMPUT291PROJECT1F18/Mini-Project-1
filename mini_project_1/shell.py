#!/usr/bin/python
# -*- coding: utf-8 -*-

"""command shell for mini-project-1"""

import cmd
import sqlite3
from getpass import getpass
from logging import getLogger

import pendulum

from mini_project_1.book_member import get_book_member_parser, book_member
from mini_project_1.cancel_booking import get_cancel_booking_parser
from mini_project_1.common import ShellArgumentException, \
    MINI_PROJECT_DATE_FMT, get_location_id, ValueNotFoundException, get_selection, send_message, check_valid_email, \
    check_valid_lcode
from mini_project_1.delete_request import get_delete_request_parser
from mini_project_1.loginsession import LoginSession
from mini_project_1.register import valid_password, \
    register_member, valid_name, valid_phone, valid_email
from mini_project_1.offer_ride import get_offer_ride_parser, check_valid_cno, offer_ride
from mini_project_1.post_request import get_post_request_parser
from mini_project_1.search_requests import \
    get_search_requests_city_parser, \
    get_search_requests_lcode_parser, print_5_and_prompt
from mini_project_1.search_rides import get_search_for_ride_parser
from mini_project_1.select_request import get_select_request_parser

__log__ = getLogger(__name__)


def logged_in(f):
    """Annotation to check if someone is logged in before attempting a
    command in the :class:`.MainProjectShell`"""
    def wrapper(*args):
        if args[0].login_session:
            return f(*args)
        else:
            __log__.error("you must be logged in to use this function")
    return wrapper


class MiniProjectShell(cmd.Cmd):
    """Main shell for mini-project-1"""
    intro = \
        "Welcome to mini-project-1 shell. Type help or ? to list commands\n"
    prompt = "mini-project-1>"
    login_session: LoginSession = None

    def __init__(self, database: sqlite3.Connection,
                 register_start: bool = False):
        """Initialize the mini-project-1 shell

        :param database: :class:`sqlite3.Connection` to the database to
        interact with the mini-project-1 shell
        """
        super().__init__()
        self.database = database
        self.register_start = register_start

    def cmdloop(self, intro=None):
        # start a login command at start.
        if self.register_start:
            self.do_register(None)
        self.do_login(None)
        super().cmdloop()

    # ===============================
    # Shell command definitions
    # ===============================

    def do_login(self, arg):
        """Login to the mini-project-1 database: login"""
        if self.login_session:
            __log__.error("already logged in")
        else:
            print("Login to mini-project-1 database:")
            username = str(input("username: "))
            password = getpass("password: ")
            self.login(username, password)
            while not self.login_session:
                self.do_login(None)
            self.do_show_inbox(None)

    @logged_in
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

    @logged_in
    def do_show_inbox(self, arg):
        """View all inbox messages related to the currently logged in email

        Set all viewed messages as seen="y"
        """
        # view all messages within your inbox
        inbox_items = self.database.execute(
            "SELECT DISTINCT email, msgTimestamp, sender, content, rno, seen "
            "FROM inbox "
            "WHERE inbox.email = ? AND inbox.seen = 'n'",
            (self.login_session.get_email(),)
        ).fetchall()

        if inbox_items:
            print("Your inbox:")
            for inbox_item in inbox_items:
                print(inbox_item)

            # set all messages within your inbox as seen="y"
            self.database.execute(
                "UPDATE inbox "
                "SET seen='y' " 
                "WHERE inbox.email = ?",
                (self.login_session.get_email(),)
            )
            self.database.commit()
        else:
            print("No new messages")

    @logged_in
    def do_offer_ride(self, arg):
        """Offer a ride"""
        dbcursor = self.database.cursor()
        parser = get_offer_ride_parser()
        try:
            args = parser.parse_args(arg.split())
            try:
                source = get_location_id(dbcursor, args.src, "Choose a source: ")
                destination = get_location_id(dbcursor, args.dst, "Choose a destination: ")
            except ValueNotFoundException as e:
                print(e)
                raise ShellArgumentException

            enroute = set()
            for place in args.enroute:
                try:
                    enroute.add(get_location_id(dbcursor, place, "Which place did you want to add? "))
                except ValueNotFoundException as e:
                    print(e)

            if not check_valid_cno(dbcursor, args.cno, self.login_session):
                args.cno = None

            if offer_ride(self.database, self.login_session, args.date.to_datetime_string(), args.seats, args.price,
                       args.luggage, source, destination, args.cno, enroute):
                print("Added ride")
            else:
                print("Could not add ride")
        except ShellArgumentException:
            __log__.error("invalid offer_ride argument")

    def help_offer_ride(self):
        """Parser help message for offering a ride"""
        parser = get_offer_ride_parser()
        parser.print_help()

    @logged_in
    def do_search_rides(self, arg):
        """Search for ride"""
        dbcursor = self.database.cursor()
        parser = get_search_for_ride_parser()
        try:
            args = parser.parse_args(arg.split())
            search_conditions = "(l1.lcode = ? OR l1.city LIKE ? OR l1.prov LIKE ? OR l1.address LIKE ? OR " + \
                "l2.lcode = ? OR l2.city LIKE ? OR l2.prov LIKE ? OR l2.address LIKE ? OR " + \
                "l3.lcode = ? OR l3.city LIKE ? OR l3.prov LIKE ? OR l3.address LIKE ?)"

            # setup query conditions for one term
            search_string = search_conditions
            search_vars = (args.term1, '%'+args.term1+'%', '%'+args.term1+'%', '%'+args.term1+'%',
                           args.term1, '%'+args.term1+'%', '%'+args.term1+'%', '%'+args.term1+'%',
                           args.term1, '%'+args.term1+'%', '%'+args.term1+'%', '%'+args.term1+'%')
            # add query conditions for the second term if supplied
            if args.term2:
                search_string = search_string + " AND " + search_conditions
                more_search_vars = (args.term2, '%'+args.term2+'%', '%'+args.term2+'%', '%'+args.term2+'%',
                                    args.term2, '%'+args.term2+'%', '%'+args.term2+'%', '%'+args.term2+'%',
                                    args.term2, '%'+args.term2+'%', '%'+args.term2+'%', '%'+args.term2+'%')
                search_vars = search_vars + more_search_vars

            # add query conditions for the third term if supplied
            if args.term3:
                search_string = search_string + " AND " + search_conditions
                more_search_vars = (args.term3, '%'+args.term3+'%', '%'+args.term3+'%', '%'+args.term3+'%',
                                    args.term3, '%'+args.term3+'%', '%'+args.term3+'%', '%'+args.term3+'%',
                                    args.term3, '%'+args.term3+'%', '%'+args.term3+'%', '%'+args.term3+'%')
                search_vars = search_vars + more_search_vars

            query = "SELECT r.* " + \
                    "FROM locations l1, locations l2, rides r " + \
                    "LEFT JOIN enroute en on en.rno = r.rno " + \
                    "LEFT JOIN locations l3 on en.lcode = l3.lcode " + \
                    "WHERE l1.lcode = r.src AND l2.lcode = r.dst AND "+search_string+";"

            dbcursor.execute(query, search_vars)
            results = dbcursor.fetchall()

            # display matching
            if len(results):
                selection = get_selection(results)
                # message the posting ride member
                if selection:
                    send_message(self.database, selection[7], self.login_session.get_email(),
                                 "I want to book seats on this ride", selection[0])
                    print("Message sent to driver")
            else:
                print("No results")
        except ShellArgumentException:
            __log__.error("invalid search_rides argument")

    def help_search_rides(self):
        """Parser help message for searching rides"""
        parser = get_search_for_ride_parser()
        parser.print_help()

    @logged_in
    def do_list_bookings(self, arg):
        """List all the bookings that the user offers"""
        cur = self.database.cursor()
        cur.execute(
            'SELECT DISTINCT bookings.* '
            'FROM bookings, rides '
            'WHERE rides.driver = ? '
            'AND rides.rno = bookings.rno;',
            (self.login_session.get_email(),)
        )
        rows = cur.fetchall()
        for row in rows:
            print(row)

    @logged_in
    def do_book_member(self, arg):
        """Book other members on a ride"""
        parser = get_book_member_parser()

        try:
            args = parser.parse_args(arg.split())
            # ensure valid inputs
            if not check_valid_lcode(self.database, args.pickup):
                print("Pickup locde not valid")
                raise ShellArgumentException
            if not check_valid_lcode(self.database, args.dropoff):
                print("Dropoff locde not valid")
                raise ShellArgumentException
            if not check_valid_email(self.database, args.email):
                print("Email not valid")
                raise ShellArgumentException

            # list my rides
            cur = self.database.cursor()
            cur.execute(
                'SELECT * '
                'FROM rides '
                'WHERE rides.driver = ?;',
                (self.login_session.get_email(),)
            )
            rows = cur.fetchall()
            ride = get_selection(rows, "Enter the row number for the ride: ")
            rno = ride[0]
            seats_available = ride[3]

            # check how many seats booked
            cur.execute(
                'SELECT sum(seats) '
                'FROM bookings '
                'WHERE bookings.rno = ?;',
                (rno,)
            )
            seats_taken = cur.fetchone()[0]
            if not seats_taken:
                seats_taken = 0

            # book seats if available or user accepts overbooking
            if seats_available < seats_taken + args.seats:
                if str(input("Warning: ride will be overbooked. Continue: [y] or [n]") == 'y'):
                    book_member(self.database, rno, args.email, args.seats, args.price, args.pickup, args.dropoff)
                    send_message(self.database, args.email, self.login_session.get_email(),
                                 "I have booked you on a ride", rno)
            else:
                book_member(self.database, rno, args.email, args.seats, args.price, args.pickup, args.dropoff)
                send_message(self.database, args.email, self.login_session.get_email(),
                             "I have booked you on a ride", rno)
        except ShellArgumentException:
            __log__.error("invalid book_member argument")

    def help_book_member(self):
        """Parser help message for booking a member"""
        parser = get_search_for_ride_parser()
        parser.print_help()

    @logged_in
    def do_cancel_booking(self, arg):
        """Cancel a booking"""
        cur = self.database.cursor()
        parser = get_cancel_booking_parser()
        try:
            args = parser.parse_args(arg.split())
            cur.execute(
                "SELECT bookings.* "
                "FROM bookings, rides "
                "WHERE bookings.bno = ? "
                "AND rides.driver = ? "
                "AND bookings.rno = rides.rno",
                (args.bno, self.login_session.get_email(),)
            )
            to_delete = cur.fetchone()

            if len(to_delete) == 0:
                print("You don't have a booking where bno={}".format(args.bno))
                print("Your bookings:")
                self.do_list_bookings(self)
                return

            cur.execute(
                "DELETE FROM bookings "
                "WHERE EXISTS("
                "SELECT * "
                "FROM bookings b2, rides "
                "WHERE b2.bno = ?"
                "AND bookings.bno = b2.bno "
                "AND rides.driver = ?"
                "AND b2.rno = rides.rno)",
                (args.bno, self.login_session.get_email(),)
            )

            self.database.commit()
            print("Successfully deleted:\n{}".format(to_delete))
            cur.execute(
                "INSERT INTO inbox VALUES (?, ?, ?, ?, ?, ?);",
                (to_delete[1], pendulum.now().to_datetime_string(),
                 self.login_session.get_email(), "Your booking has been cancelled.",
                 to_delete[2], "n")
            )
            self.database.commit()
            print("Successfully sent cancellation message to {}."
                  .format(to_delete[1]))
        except ShellArgumentException:
            __log__.exception("invalid cancel_booking argument")

    def help_cancel_booking(self):
        """Parser help message for cancelling a booking"""
        parser = get_cancel_booking_parser()
        parser.print_help()

    @logged_in
    def do_post_request(self, arg):
        """Post a ride request"""
        parser = get_post_request_parser()
        try:
            args = parser.parse_args(arg.split())

            # generate a new rid
            max_rid = self.database.execute(
                "select max(r.rid) from requests r").fetchone()[0]
            if not max_rid:
                max_rid = 0
            rid = 1 + int(max_rid)

            # validate the given location codes
            self.validate_location_code(args.pickup)
            self.validate_location_code(args.dropoff)

            # create and insert the new ride request
            self.database.execute(
                "INSERT INTO requests VALUES (?, ?, ?, ?, ?, ?)",
                (rid, self.login_session.get_email(),
                 args.date.strftime(MINI_PROJECT_DATE_FMT),
                 args.pickup, args.dropoff, args.price)
            )
            self.database.commit()
        except ShellArgumentException:
            __log__.exception("invalid post_ride_request argument")
        else:
            __log__.info(
                "succesfully posted ride request: "
                "rid: {} email: {} date: {} pickup: {} dropoff: {} price: {}".format(
                    rid, self.login_session.get_email(),
                    args.date.strftime(MINI_PROJECT_DATE_FMT),
                    args.pickup, args.dropoff, args.price
                )
            )

    def help_post_request(self):
        """Post a ride request's parsers help message"""
        parser = get_post_request_parser()
        parser.print_help()

    @logged_in
    def do_list_requests(self, arg):
        """List all the user's ride requests"""
        cur = self.database.cursor()
        cur.execute(
            'SELECT DISTINCT * ' 
            'FROM requests ' 
            'WHERE email = ?',
            (self.login_session.get_email().lower(),)
        )
        rows = cur.fetchall()
        for row in rows:
            print(row)

    @logged_in
    def do_search_requests_lcode(self, arg):
        """Search for a ride request by location number"""
        cur = self.database.cursor()
        parser = get_search_requests_lcode_parser()

        try:
            args = parser.parse_args(arg.split())
            cur.execute(
                'SELECT DISTINCT requests.* '
                'FROM requests '
                'WHERE pickup = ?',
                (args.lcode,)
            )
            rows = cur.fetchall()
            print_5_and_prompt(rows)
        except ShellArgumentException:
            __log__.exception("invalid argument")

    def help_search_requests_lcode(self):
        """Parser help message for searching ride requests by location code"""
        parser = get_search_requests_lcode_parser()
        parser.print_help()

    @logged_in
    def do_search_requests_city(self, arg):
        """Search for a ride quest by city name"""
        cur = self.database.cursor()
        parser = get_search_requests_city_parser()

        try:
            args = parser.parse_args(arg.split())
            cur.execute(
                'SELECT DISTINCT requests.* '
                'FROM requests, locations '
                'WHERE requests.pickup = locations.lcode '
                'AND locations.city = ?',
                (args.city.lower(),)
            )
            rows = cur.fetchall()
            print_5_and_prompt(rows)
        except ShellArgumentException:
            __log__.exception("invalid argument")

    def help_search_requests_city(self):
        """Parser help message for searching ride requests by city name"""
        parser = get_search_requests_city_parser()
        parser.print_help()

    @logged_in
    def do_delete_request(self, arg):
        """Delete a ride request"""
        cur = self.database.cursor()
        parser = get_delete_request_parser()

        try:
            args = parser.parse_args(arg.split())
            cur.execute(
                "SELECT DISTINCT * "
                "FROM requests " 
                "WHERE rid = ? AND email = ?",
                (args.rid, self.login_session.get_email(),)
            )
            to_delete = cur.fetchall()

            if len(to_delete) == 0:
                print("You don't have a ride request where rid={}"
                      .format(args.rid))
                print("Your requests:")
                self.do_list_requests(self)
                return

            cur.execute(
                "DELETE "
                "FROM requests "
                "WHERE rid = ? AND email = ?",
                (args.rid, self.login_session.get_email(),)
            )
            self.database.commit()

            print("Successfully deleted:\n{}".format(to_delete))
        except ShellArgumentException:
            __log__.exception("invalid argument")

    def help_delete_request(self):
        """Parser help message for deleting a ride request"""
        parser = get_delete_request_parser()
        parser.print_help()

    @logged_in
    def do_select_request(self, arg):
        """Select a ride request and perform actions"""
        cur = self.database.cursor()
        parser = get_select_request_parser()

        try:
            args = parser.parse_args(arg.split())
            cur.execute(
                "SELECT * "
                "FROM requests "
                "WHERE rid = ?",
                (args.rid,)
            )
            selected = cur.fetchone()

            print("You have selected: {}".format(selected))
            while True:
                response = \
                    input("Would you like to message the poster? [y|n]\n")
                if response == "y":
                    message = input("Your message: ")
                    cur.execute(
                        "SELECT email "
                        "FROM requests "
                        "WHERE rid = ?",
                        (args.rid,)
                    )
                    poster = cur.fetchone()[0]

                    cur.execute(
                        "INSERT INTO inbox VALUES (?, ?, ?, ?, ?, ?);",
                        (poster,
                         pendulum.now().to_datetime_string(),
                         self.login_session.get_email(),
                         message,
                         0,  # TODO: What to put here? - A none value.
                         "n")
                    )
                    self.database.commit()
                    break
                elif response == "n":
                    break
        except ShellArgumentException:
            __log__.error("invalid argument")

    def help_select_request(self):
        """Parser help message for selecting a ride request"""
        parser = get_select_request_parser()
        parser.print_help()

    def do_register(self, arg):
        """Register a new member to the mini-project-1 database"""
        # get a valid email
        print("Starting member registration wizard:")
        while True:
            email_str = input("email: ")
            if valid_email(self.database, email_str):
                email_str = valid_email(self.database, email_str)
                break

        # get valid name
        while True:
            name_str = input("name: ")
            if valid_name(name_str):
                break

        # get valid phone
        while True:
            phone_str = input("phone: ")
            if valid_phone(phone_str):
                phone_str = valid_phone(phone_str)
                break

        # get valid password
        while True:
            password1 = getpass("password: ")
            if not valid_password(password1):
                continue
            password2 = getpass("validate password: ")
            if password1 != password2:
                print("passwords do not match")
                continue
            else:
                break

        # finally register the new user
        register_member(
            self.database, email_str, name_str, phone_str, password1)

    # ===============================
    # Shell functionality definitions
    # ===============================

    @logged_in
    def logout(self):
        """Logout method

        Set the shell's ``login_session`` to :obj:`None`.
        """
        email = self.login_session.get_email()
        self.login_session = None
        __log__.info("logged out user: {}".format(email))

    def login(self, email: str, password: str):
        """Login method

        Check if a :class:`LoginSession` already exists for the shell if not
        attempt to login with the given email and password.

        If the login attempt is successful set the shell's ``login_session``
        to the newly created :class:`LoginSession`.
        """
        if self.login_session:
            __log__.error("already logged in as user: {}".format(
                self.login_session.get_email()))
        else:
            user_hit = self.database.execute(
                "SELECT email, pwd "
                "FROM members "
                "WHERE email = ? AND pwd = ?",
                (email.lower(), password)
            ).fetchone()
            if user_hit:
                self.login_session = LoginSession(user_hit[0], user_hit[1])
                __log__.info("logged in user: {}".format(user_hit[0]))
            else:
                __log__.warning("invalid login: bad username/password")

    # TODO: this should be moved outside if possible - see check_valid_lcode in common
    def validate_location_code(self, location_code_str: str):
        """Validate that a location ode for use in ``post_ride_request``
        command actually exists in locations

        :raises: :class:`ShellArgumentException` if the given location code
                 is not within the ``locations`` table.
        """

        locations = self.database.execute(
            "SELECT lcode "
            "FROM locations "
            "WHERE locations.lcode = ?",
            (location_code_str,)
        ).fetchone()
        if not locations:
            raise ShellArgumentException(
                "invalid location code: {}".format(location_code_str))

