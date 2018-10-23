#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Class representing a member"""

from logging import getLogger

__log__ = getLogger(__name__)


class Member:
    """Class representing a member"""

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
