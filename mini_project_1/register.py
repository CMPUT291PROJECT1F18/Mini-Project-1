#!/usr/bin/python
# -*- coding: utf-8 -*-

"""allow users to register.py to the mini-project-1 database"""

import argparse
import re
import sqlite3
from email.utils import parseaddr
from logging import getLogger

__log__ = getLogger(__name__)


def check_valid_email(database: sqlite3.Connection, email: str) -> bool:
    """Check if a given email is unique to the mini-project-1 database"""
    email_hits = database.execute("SELECT email from members where email = ?", (email, )).fetchone()
    print(email_hits)
    if email_hits:
        return False
    else:
        return True


def password(password_str: str) -> str:
    """Argparse type validator for a member's password"""
    if 6 < len(password_str) < 1:
        raise argparse.ArgumentTypeError("invalid password length: choose between 1 to 6 characters")
    else:
        return password_str


def phone(phone_str: str) -> str:
    """Argparse type validator for a member's phone number"""
    m = re.search("(\d{3})?(?: ?|-?)(\d{3})(?: ?|-?)(\d{4})", phone_str)
    try:
        return "{}-{}-{}".format(m.group(1), m.group(2), m.group(3))
    except AttributeError:
        raise argparse.ArgumentTypeError("invalid phone number: please use format: XXX-XXX-XXXX")


def email(email_str: str) -> str:
    """Argparse type validator for a member's email"""
    full_name, email_addr = parseaddr(email_str)
    if not email_addr:
        raise argparse.ArgumentTypeError("invalid email: please use format: name@addr")
    elif 15 < len(email_addr) < 3:
        raise argparse.ArgumentTypeError("invalid email length: choose between 3 to 15 characters")
    else:
        return email_addr


def name(name_str: str) -> str:
    """Argparse type validator for a member's name"""
    if 20 < len(name_str) < 0:
        raise argparse.ArgumentTypeError("invalid name length: choose between 1 to 20 characters")
    else:
        return name_str


def register_member(database: sqlite3.Connection, email: str, name: str, phone: str, password: str):
    """Register a new member into the mini-project-1 database"""
    if check_valid_email(database, email):
        database.execute("INSERT INTO members VALUES (?, ?, ?, ?)", email, name, phone, password)
        database.commit()
    else:
        __log__.error("email {} already taken: please choose an alternative".format(email))
