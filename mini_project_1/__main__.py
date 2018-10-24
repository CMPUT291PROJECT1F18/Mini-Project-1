#!/usr/bin/python
# -*- coding: utf-8 -*-

"""argparse and entry point script for mini-project-1"""

import argparse
import os
import sys
import sqlite3
import logging
from logging import getLogger, basicConfig, Formatter
from logging.handlers import TimedRotatingFileHandler

from mini_project_1.shell import MiniProjectShell

__log__ = getLogger(__name__)

LOG_LEVEL_STRINGS = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]


def log_level(log_level_string):
    if log_level_string not in LOG_LEVEL_STRINGS:
        raise argparse.ArgumentTypeError(
            "invalid choice: {} (choose from {})".format(
                log_level_string,
                LOG_LEVEL_STRINGS
            )
        )
    return getattr(logging, log_level_string, logging.INFO)


DATABASE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
DATABASE_TABLE_CREATE = os.path.join(DATABASE_DIR, "create_tables.sql")
DATABASE_DATA_CREATE = os.path.join(DATABASE_DIR, "create_data.sql")


def init_db(filename: str):
    """Create a example database for mini-project-1"""
    database = sqlite3.connect(filename)
    cursor = database.cursor()
    # Create the tables
    cursor.executescript(open(DATABASE_TABLE_CREATE, "r").read())
    # Insert data
    cursor.executescript(open(DATABASE_DATA_CREATE, "r").read())
    # Save (commit) the changes
    database.commit()


def get_parser() -> argparse.ArgumentParser:
    """Create and return the argparser for mini-project-1"""
    parser = argparse.ArgumentParser(
        description="Start the mini-project-1 shell"
    )

    group = parser.add_argument_group(title="Database")
    group = group.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--database",
                       help="Path to an existing SQLITE database file "
                            "or mini-project-1 to connect to")
    group.add_argument("-i", "--init-database",
                       dest="init_database",
                       help="Create a example SQLITE database file "
                            "for mini-project-1 at the path specified "
                            "and connect to it")

    group = parser.add_argument_group(title="Logging")
    group.add_argument("--log-level", dest="log_level", default="INFO",
                       type=log_level, help="Set the logging output level")
    group.add_argument("--log-dir", dest="log_dir",
                       help="Enable TimeRotatingLogging at the directory "
                            "specified")
    group.add_argument("-v", "--verbose", action="store_true",
                       help="Enable verbose logging")

    return parser


def main(argv=sys.argv[1:]):
    """main entry point mini-project-1"""
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

    basicConfig(
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

    __log__.info("starting mini-project-1 shell")
    MiniProjectShell(conn).cmdloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
