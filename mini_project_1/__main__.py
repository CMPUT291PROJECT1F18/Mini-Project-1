#!/usr/bin/python
# -*- coding: utf-8 -*-

"""argparse script for mini-project-1"""

import argparse
import sys


def get_parser():
    """Create and return the argparser for mini-project-1"""
    parser = argparse.ArgumentParser(
        description="example argument parser"
    )
    parser.add_argument("-e1", help="example arg 1")

    group = parser.add_argument_group("example group 1")
    group.add_argument("-e2", help="example arg 2")

    return parser


def main(argv=sys.argv[1:]):
    """argparse function for mini-project-1"""
    parser = get_parser()
    args = parser.parse_args(argv)

    return 0


if __name__ == "__main__":
    sys.exit(main())
