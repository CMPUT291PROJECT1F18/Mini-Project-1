#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Class representing a member"""

from logging import getLogger

__log__ = getLogger(__name__)


class LoginSession:
    """Class representing a member"""

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def get_email(self):
        return self.email
