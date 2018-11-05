#!/usr/bin/python
# -*- coding: utf-8 -*-

"""common utilities utilized by mini-project-1"""

import argparse
import sqlite3
import sys

import pendulum

MINI_PROJECT_DATE_FMT = "%Y-%m-%d"


class ShellArgumentException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class ShellArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help(sys.stderr)
        raise ShellArgumentException(message)


def price(price_string: str) -> int:
    price = int(price_string)
    if price < 0:
        raise argparse.ArgumentTypeError(
            "invalid price: {} (please choose a non negative price)".format(
                price_string
            )
        )
    return price


def greater_than_zero_number(value: str) -> int:
    value = int(value)
    if value <= 0:
        raise argparse.ArgumentTypeError("%s must be a greater than zero number" % value)
    return value


def date(date_str: str) -> pendulum.DateTime:
    return pendulum.parse(date_str)


class ValueNotFoundException(Exception):
    """Exception for queries with no results"""
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


def get_selection(items: list, prompt: str= "Enter selection number: "):
    """Gets the user to select a item from a list, displaying up to 5 items
    at a time.

    :param items: list of items
    :param prompt: a prompt for user input, default is "Enter selection number: "
    :return: selected item from items
    """
    index = 0
    while True:
        print("%i: %s" % (index, items[index]))

        if index % 5 == 4:
            print("Press Enter to see more\n")
            selection = str(input(prompt))

            if selection.isnumeric():
                selection = int(selection)
                if -1 < selection < len(items):
                    return items[selection]
            elif selection == "exit":
                return None
        elif index + 1 == len(items):
            print("Press Enter to return to the start of the list\n")
            selection = str(input(prompt))

            if selection.isnumeric():
                selection = int(selection)
                if -1 < selection < len(items):
                    return items[selection]
            elif selection == "exit":
                return None
            index = -1
            print("An entry must be selected")
        index += 1


def get_location_id(dbcursor: sqlite3.Cursor, keyword: str, prompt: str = None):
    """Gets a location lcode from the user."""

    # get exact match locde
    dbcursor.execute(
        "SELECT * FROM locations WHERE lcode = ?", (keyword,))
    location = dbcursor.fetchall()
    if location:
        return location[0][0]

    # get matching locations, since it's not a lcode
    kw = '%' + keyword + '%'
    dbcursor.execute(
        "SELECT * FROM locations WHERE city LIKE ? OR prov LIKE ? OR address LIKE ?",
        (kw, kw, kw))
    locations = dbcursor.fetchall()

    # display and get user selection if more than one
    if len(locations) > 1:
        if prompt:
            print(prompt)
        return get_selection(locations)[0]
    elif locations:
        return locations[0][0]
    else:
        raise ValueNotFoundException("No location for " + keyword)


def send_message(database: sqlite3.Connection, recipient: str, sender: str, content: str, rno: int):
    """"""
    cur = database.cursor()

    send_query = "INSERT INTO inbox VALUES (?, ?, ?, ?, ?, ?);"
    cur.execute(send_query,
                (recipient, pendulum.now().to_datetime_string(),
                 sender, content, rno, "n"))
    database.commit()


def check_valid_lcode(database: sqlite3.Connection, lcode: str):
    """Checks whether a lcode is in the database"""
    dbcursor = database.cursor()
    dbcursor.execute(
        "SELECT * FROM locations WHERE lcode = ?", (lcode,))
    if dbcursor.fetchall():
        return True
    return False


def check_valid_email(database: sqlite3.Connection, email: str):
    """Checks whether an email is in the database"""
    dbcursor = database.cursor()
    dbcursor.execute(
        "SELECT * FROM members WHERE email = ?", (email,))
    if dbcursor.fetchall():
        return True
    return False
