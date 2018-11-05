#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Show inbox

After a login, all unseen messages of the member will be displayed, and the
status of the messages will be set to seen (i.e, the seen column is set
to 'y').
"""

from mini_project_1.common import ShellArgumentParser


def get_show_inbox_parser() -> ShellArgumentParser:
    """Argparser for the :class:`.shell.MiniProjectShell`
    ``show_inbox`` command"""
    parser = ShellArgumentParser(
        prog="show_inbox",
        add_help=False,
        description="List all the unseen messages in your inbox")

    return parser
