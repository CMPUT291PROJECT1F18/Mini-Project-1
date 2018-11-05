#!/usr/bin/python
# -*- coding: utf-8 -*-

"""common utilities utilized by mini-project-1"""

import argparse
import sys


MINI_PROJECT_DATE_FMT = "%Y-%m-%d"


class ShellArgumentException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


class ShellArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help(sys.stderr)
        raise ShellArgumentException(message)
