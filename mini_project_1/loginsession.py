#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Class representing a logged in session to the mini-project-1 database"""

from logging import getLogger

__log__ = getLogger(__name__)


class LoginSession:
    """Class representing a logged in session to the mini-project-1 database"""

    def __init__(self, email: str, password: str):
        self._email = email
        self._password = password

    def get_email(self) -> str:
        return self._email
