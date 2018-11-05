#!/usr/bin/python
# -*- coding: utf-8 -*-

"""pytests interacting with databases for mini-project-1"""

import os
import sqlite3
import pytest
from mock import mock

import mini_project_1
from mini_project_1.book_member import book_member
from mini_project_1.common import send_message
from mini_project_1.loginsession import LoginSession
from mini_project_1.offer_ride import offer_ride
from mini_project_1.post_request import valid_location_code
from mini_project_1.shell import MiniProjectShell
from mini_project_1.register import valid_email, valid_password, valid_name, \
    valid_phone, register_member
from unittest import TestCase

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


def test_register(mock_db):
    """"""
    database = sqlite3.connect(mock_db)
    dbcursor = database.cursor()
    shell = MiniProjectShell(database)
    testcases = list()

    prev_all_members = dbcursor.execute("Select * from members").fetchall()

    register_member(database, "bob@456.ca", "Jonny Boi", '213-342-2834', 'pass')
    register_member(database, "vali@mail.com", "Jonny Boi", '213-342-2834', 'pass')
    register_member(database, "val@mail.com", "Jonny Boi", '213-342-2834', 'pass')

    all_members = dbcursor.execute("Select * from members").fetchall()
    assert len(prev_all_members) + 3 == len(all_members)


# def test_select_request(mock_db): TODO
#     """"""
#     pass


def test_delete_request(mock_db):
    """Tests delete request"""
    database = sqlite3.connect(mock_db)
    shell = MiniProjectShell(database)
    shell.login("bob@123.ca", "foo")

    assert database.cursor().execute("SELECT DISTINCT * FROM requests WHERE rid = 15").fetchone()
    shell.do_delete_request('15')
    assert not database.cursor().execute("SELECT DISTINCT * FROM requests WHERE rid = 15").fetchone()
    assert database.cursor().execute("SELECT DISTINCT * FROM requests WHERE rid = 16").fetchone()
    shell.do_delete_request('16')
    assert not database.cursor().execute("SELECT DISTINCT * FROM requests WHERE rid = 16").fetchone()


# def test_search_requests_city(mock_db): TODO
#     pass


# def test_search_requests_lcode(mock_db): TODO
#     pass


# def test_list_requests(mock_db):
#     database = sqlite3.connect(mock_db)
#     shell = MiniProjectShell(database)
#     shell.login("bob@123.ca", "foo")


def test_post_request(mock_db):
    database = sqlite3.connect(mock_db)
    shell = MiniProjectShell(database)
    shell.login("bob@123.ca", "foo")
    assert not database.cursor().execute("SELECT DISTINCT * FROM requests "
                                         "WHERE email = 'bob@123.ca' AND dropoff = 'cntr3'").fetchone()
    shell.do_post_request("2018-12-31 west1 cntr3 1000")
    assert database.cursor().execute("SELECT DISTINCT * FROM requests "
                                     "WHERE email = 'bob@123.ca' AND dropoff = 'cntr3'").fetchone()


def test_cancel_booking(mock_db):
    database = sqlite3.connect(mock_db)
    shell = MiniProjectShell(database)
    shell.login("bob@123.ca", "foo")
    assert database.cursor().execute("SELECT DISTINCT * FROM bookings "
                                     "WHERE bno = 13").fetchone()
    shell.do_cancel_booking("13")
    assert not database.cursor().execute("SELECT DISTINCT * FROM bookings "
                                         "WHERE bno = 13").fetchone()


def test_book_member(mock_db):
    database = sqlite3.connect(mock_db)
    shell = MiniProjectShell(database)
    shell.login("bob@123.ca", "foo")
    assert not database.cursor().execute("SELECT DISTINCT * FROM bookings "
                                         "WHERE email like 'jane_doe@abc.ca'").fetchone()

    book_member(database, 44, 'jane_doe@abc.ca', 12000, 1, 'west1', 'yyc1')

    assert database.cursor().execute("SELECT DISTINCT * FROM bookings "
                                     "WHERE email like 'jane_doe@abc.ca'").fetchone()


# def test_list_bookings(mock_db): TODO
#     database = sqlite3.connect(mock_db)
#     shell = MiniProjectShell(database)
#     shell.login("bob@123.ca", "foo")


# def test_search_rides(mock_db): TODO
#     database = sqlite3.connect(mock_db)
#     shell = MiniProjectShell(database)
#     shell.login("bob@123.ca", "foo")


def test_offer_ride(mock_db):
    database = sqlite3.connect(mock_db)
    shell = MiniProjectShell(database)
    user = LoginSession("jane_doe@abc.ca", "")
    shell.login("jane_doe@abc.ca", "")
    assert not database.cursor().execute("SELECT DISTINCT * FROM rides "
                                         "WHERE rno > 43 AND driver LIKE 'jane_doe@abc.ca'").fetchone()
    offer_ride(database, user, "2018-12-31", 3, 3000, "I love em", 'west1', 'ab1', 1, {'cntr1', 'cntr2', 'cntr3'})
    assert database.cursor().execute("SELECT DISTINCT * FROM rides "
                                     "WHERE rno > 43 AND driver LIKE 'jane_doe@abc.ca'").fetchone()


def test_send_message(mock_db):
    database = sqlite3.connect(mock_db)
    shell = MiniProjectShell(database)

    assert not database.cursor().execute("SELECT * FROM inbox "
                                         "WHERE email LIKE 'jane_doe@abc.ca'").fetchall()
    send_message(database, 'jane_doe@abc.ca', 'bob@123.ca', 'I love you', 42)

    assert database.cursor().execute("SELECT * FROM inbox "
                                     "WHERE email LIKE 'jane_doe@abc.ca'").fetchall()


def test_show_inbox(mock_db):
    database = sqlite3.connect(mock_db)
    shell = MiniProjectShell(database)
    shell.login("bob@123.ca", "foo")
    unread_mail = database.cursor().execute("SELECT DISTINCT * "
                "FROM inbox "
                "WHERE inbox.email = 'bob@123.ca' AND inbox.seen = 'n'").fetchall()
    shell.do_show_inbox(None)
    read_mail = database.cursor().execute("SELECT DISTINCT * "
                "FROM inbox "
                "WHERE inbox.email = 'bob@123.ca' AND inbox.seen = 'y'").fetchall()

    assert len(unread_mail) == len(read_mail)

    assert not database.cursor().execute("SELECT DISTINCT * "
                "FROM inbox "
                "WHERE inbox.email = 'bob@123.ca' AND inbox.seen = 'n'").fetchall()



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
    shell.help_list_bookings()
    shell.help_list_requests()
    shell.help_logout()


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


def test_valid_location_code_valid(mock_db):
    database = sqlite3.connect(mock_db)
    assert valid_location_code(database, "cntr1")


def test_valid_location_code_invalid(mock_db):
    database = sqlite3.connect(mock_db)
    assert not valid_location_code(database, "INVALID_LOCATION_CODE")
