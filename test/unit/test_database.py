#!/usr/bin/python
# -*- coding: utf-8 -*-

"""pytests interacting with databases for mini-project-1"""

import os
import sqlite3
import pytest
import mini_project_1
from mini_project_1.shell import MiniProjectShell
from mini_project_1.register import valid_email, valid_password, valid_name, \
    valid_phone

DATABASE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(mini_project_1.__file__)),
    "data",
)

DATABASE_TABLE_CREATE = os.path.join(DATABASE_DIR, "create_tables.sql")
DATABASE_DATA_CREATE = os.path.join(DATABASE_DIR, "create_data.sql")


def create_test_db(filename: str):
    """Create a test database"""
    database = sqlite3.connect(filename)
    cursor = database.cursor()
    # Create the tables
    cursor.executescript(open(DATABASE_TABLE_CREATE, "r").read())
    # Insert data
    cursor.executescript(open(DATABASE_DATA_CREATE, "r").read())
    # Save (commit) the changes
    database.commit()


@pytest.fixture(scope="session")
def mock_db(tmpdir_factory):
    """pytest fixture returning the path to a mock database for testing"""
    filename = str(tmpdir_factory.mktemp("data").join("test.db"))
    create_test_db(filename)
    return filename


def test_example(mock_db):
    """Test example for interacting with data mocks"""
    database = sqlite3.connect(mock_db)
    print(database.execute("""SELECT name FROM members""").fetchall())

###############################
# tests related to shell.py
###############################


def test_login(mock_db):
    database = sqlite3.connect(mock_db)
    shell = MiniProjectShell(database)
    assert not shell.login_session
    shell.login("bob@123.ca", "foo")
    assert shell.login_session
    assert shell.login_session.get_email() == "bob@123.ca"
    assert shell.login_session._email == "bob@123.ca"
    assert shell.login_session._password == "foo"


def test_logout(mock_db):
    database = sqlite3.connect(mock_db)
    shell = MiniProjectShell(database)
    assert not shell.login_session
    shell.login("bob@123.ca", "foo")
    assert shell.login_session
    shell.logout()
    assert not shell.login_session


def test_help_messsages(mock_db):
    """Test all the shell's ``help_<command>`` methods

    Ensure that they can be called without raising an exception.
    """
    database = sqlite3.connect(mock_db)
    shell = MiniProjectShell(database)

    shell.help_book_member()
    shell.help_cancel_booking()
    shell.help_delete_request()
    shell.help_search_requests_lcode()
    shell.help_search_requests_city()
    shell.help_search_rides()
    shell.help_select_request()
    shell.help_post_request()
    shell.help_offer_ride()


###############################
# tests related to register.py
###############################


def test_valid_email_valid(mock_db):
    """Test valid_email with valid emails"""
    database = sqlite3.connect(mock_db)
    # check for a valid new unique email
    assert valid_email(database, "cra@example.com")


def test_valid_email_invalid(mock_db):
    """Test valid_email with invalid emails"""
    database = sqlite3.connect(mock_db)
    # check for a invalid new unique email
    assert not valid_email(database, "")
    assert not valid_email(database, "bob@123.ca")
    assert not valid_email(database, "reallylongemail@longdomain.ca")
    assert not valid_email(database, "foobar")


def test_valid_password_valid():
    """Test valid_password with valid passwords"""
    assert valid_password("123456")
    assert valid_password("abcdef")


def test_valid_password_invalid():
    """Test valid_password with invalid passwords"""
    assert not valid_password("")
    assert not valid_password("1234567")
    assert not valid_password("abcdefg")


def test_valid_name_valid():
    """Test valid_name with valid names"""
    assert valid_name("1")
    assert valid_name("a"*20)


def test_valid_name_invalid():
    """Test valid_name with invalid names"""
    assert not valid_name("")
    assert not valid_name("a"*21)


def test_valid_phone_valid():
    """Test valid_phone with valid phone numbers"""
    assert valid_phone("000-000-0000")
    assert valid_phone("0000000000")


def test_valid_phone_invalid():
    """Test valid_phone with invalid phone numbers"""
    assert not valid_phone("")
    assert not valid_phone("000-000-00000")
    assert not valid_phone("000-0000-0000")
    assert not valid_phone("0000-000-0000")
    assert not valid_phone("00000000000")
    assert not valid_phone("foobar")
