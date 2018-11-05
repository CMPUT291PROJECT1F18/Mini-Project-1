#!/usr/bin/python
# -*- coding: utf-8 -*-

"""register a new member to a mini-project-1 database"""

import re
import sqlite3
from email.utils import parseaddr
from logging import getLogger
from typing import Union

__log__ = getLogger(__name__)


def unique_email(database: sqlite3.Connection, email: str) -> bool:
    """Check if a given email is unique to the mini-project-1 database"""
    email_hits = database.execute(
        "SELECT email "
        "FROM members "
        "WHERE email = ?",
        (email, )
    ).fetchone()
    if email_hits:
        return False
    else:
        return True


def valid_password(password_str: str) -> bool:
    """Validator for a member's password"""
    if len(password_str) < 1 or 6 < len(password_str):
        __log__.error(
            "invalid password length: choose between 1 to 6 characters")
        return False
    else:
        return True


def valid_phone(phone_str: str) -> Union[bool, str]:
    """Validator for a member's phone number"""
    m = re.search("^(\d{3})?(?: ?|-?)(\d{3})(?: ?|-?)(\d{4})$", phone_str)
    try:
        return "{}-{}-{}".format(m.group(1), m.group(2), m.group(3))
    except AttributeError:
        __log__.error("invalid phone number: please use format: XXX-XXX-XXXX")
        return False


def valid_email(database: sqlite3.Connection, email_str: str) ->\
        Union[bool, str]:
    """Validator for a member's email"""
    full_name, email_addr = parseaddr(email_str)
    if not email_addr or "@" not in email_str[1:-3]:
        __log__.error("invalid email: please use format: name@addr")
        return False
    elif len(email_addr) < 3 or 15 < len(email_addr):
        __log__.error(
            "invalid email length: choose between 3 to 15 characters")
        return False
    elif not unique_email(database, email_addr):
        __log__.error(
            "invalid email: email {} is already taken".format(email_addr))
        return False
    else:
        return email_addr


def valid_name(name_str: str) -> bool:
    """Validator for a member's name"""
    if len(name_str) < 1 or 20 < len(name_str):
        __log__.error("invalid name length: choose between 1 to 20 characters")
        return False
    else:
        return True


def register_member(database: sqlite3.Connection, email: str, name: str,
                    phone: str, password: str):
    """Register a new member into the mini-project-1 database"""
    database.execute("INSERT INTO members VALUES (?, ?, ?, ?)",
                     (email, name, phone, password))
    database.commit()
    __log__.info("registered user: email: {} name: {} phone: {}".format(
                    email, name, phone))
