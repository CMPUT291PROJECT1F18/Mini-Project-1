#!/usr/bin/python
# -*- coding: utf-8 -*-

"""argparse and entry point script for mini-project-1"""

import argparse
import sys

from mini_project_1.shell import MiniProjectShell


def get_parser():
    """Create and return the argparser for mini-project-1"""
    parser = argparse.ArgumentParser(
        description="Start the mini-project-1 shell"
    )
    return parser


def main(argv=sys.argv[1:]):
    """main entry point mini-project-1"""
    parser = get_parser()
    args = parser.parse_args(argv)
    # TODO: possibly add different startup arguments
    MiniProjectShell().cmdloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
