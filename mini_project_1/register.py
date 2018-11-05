#!/usr/bin/python
# -*- coding: utf-8 -*-

"""registration to a mini-project-1 database"""

import argparse
import logging
import os
import re
import sqlite3
import sys
from email.utils import parseaddr
from logging import getLogger, Formatter
from logging.handlers import TimedRotatingFileHandler

from mini_project_1.__main__ import get_parser as get_main_parser, init_db

__log__ = getLogger(__name__)


def check_valid_email(database: sqlite3.Connection, email: str) -> bool:
    """Check if a given email is unique to the mini-project-1 database"""
    email_hits = database.execute("SELECT email from members where email = ?", (email, )).fetchone()
    if email_hits:
        return False
    else:
        return True


def password(password_str: str) -> str:
    """Argparse type validator for a member's password"""
    if 6 < len(password_str) < 1:
        raise argparse.ArgumentTypeError(
            "invalid password length: choose between 1 to 6 characters")
    else:
        return password_str


def phone(phone_str: str) -> str:
    """Argparse type validator for a member's phone number"""
    m = re.search("(\d{3})?(?: ?|-?)(\d{3})(?: ?|-?)(\d{4})", phone_str)
    try:
        return "{}-{}-{}".format(m.group(1), m.group(2), m.group(3))
    except AttributeError:
        raise argparse.ArgumentTypeError(
            "invalid phone number: please use format: XXX-XXX-XXXX")


def email(email_str: str) -> str:
    """Argparse type validator for a member's email"""
    full_name, email_addr = parseaddr(email_str)
    if not email_addr or "@" not in email_str[1:-3]:
        raise argparse.ArgumentTypeError(
            "invalid email: please use format: name@addr")
    elif 15 < len(email_addr) < 3:
        raise argparse.ArgumentTypeError(
            "invalid email length: choose between 3 to 15 characters")
    else:
        return email_addr


def name(name_str: str) -> str:
    """Argparse type validator for a member's name"""
    if 20 < len(name_str) < 0:
        raise argparse.ArgumentTypeError(
            "invalid name length: choose between 1 to 20 characters")
    else:
        return name_str


def register_member(database: sqlite3.Connection, email: str, name: str, phone: str, password: str):
    """Register a new member into the mini-project-1 database"""
    if check_valid_email(database, email):
        database.execute("INSERT INTO members VALUES (?, ?, ?, ?)", (email, name, phone, password))
        database.commit()
        __log__.info("registered user: email: {} name: {} phone: {}".format(email, name, phone))
    else:
        raise Exception("email {} already taken: please choose an alternative".format(email))


def get_parser() -> argparse.ArgumentParser:
    """Create a custom parser based for registering users to an existing
    mini-project-1 database"""
    parser = get_main_parser()
    parser.description = \
        "register a new member to an existing mini-project-1 database"
    group = parser.add_argument_group(title='registration')
    group.add_argument("-r", "--register", action="store_true",
                       help="Enable registering a new user")
    group.add_argument("email", type=email,
                       help="A unique email to register and login with")
    group.add_argument("phone", type=phone,
                       help="A phone number to register with")
    group.add_argument("name", type=name,
                       help="A name (first and last) to register with")
    group.add_argument("password", type=password,
                       help="A password to register and login with")
    return parser


def main(argv=sys.argv[1:]):
    """entry point for registering members to an existing mini-project-1
    database"""
    parser = get_parser()
    args = parser.parse_args(argv)

    # configure logging
    handlers_ = []
    log_format = Formatter(fmt="[%(asctime)s] [%(levelname)s] - %(message)s")
    if args.log_dir:
        os.makedirs(args.log_dir, exist_ok=True)
        file_handler = TimedRotatingFileHandler(
            os.path.join(args.log_dir, "mini_project_1.log"),
            when="d", interval=1, backupCount=7, encoding="UTF-8",
        )
        file_handler.setFormatter(log_format)
        file_handler.setLevel(args.log_level)
        handlers_.append(file_handler)
    if args.verbose:
        stream_handler = logging.StreamHandler(stream=sys.stderr)
        stream_handler.setFormatter(log_format)
        stream_handler.setLevel(args.log_level)
        handlers_.append(stream_handler)

    logging.basicConfig(
        handlers=handlers_,
        level=args.log_level
    )

    # if specified initialize a example database
    if args.init_database:
        __log__.info("creating example mini-project-1 "
                     "database at: {}".format(args.init_database))
        init_db(args.init_database)

    # establish a connection to the database
    __log__.info("connecting to mini-project-1 "
                 "database at: {}".format(args.database or args.init_database))
    conn = sqlite3.connect(args.database or args.init_database)

    # attempt registration
    if args.email and args.phone and args.name and args.password:
        register_member(conn, args.email, args.name, args.phone, args.password)

    return 0


if __name__ == "__main__":
    sys.exit(main())
