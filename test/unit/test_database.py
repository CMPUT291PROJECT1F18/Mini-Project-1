#!/usr/bin/python
# -*- coding: utf-8 -*-

"""pytests interacting with databases for mini-project-1"""

import os
import sqlite3
import pytest
import mini_project_1
from mini_project_1.shell import MiniProjectShell


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


def test_login(mock_db):
    database = sqlite3.connect(mock_db)
    shell = MiniProjectShell(database)
    assert not shell.login_session
    shell.login("bob@123.ca", "foo")
    assert shell.login_session
    assert shell.login_session.email == "bob@123.ca"
    assert shell.login_session.password == "foo"


def test_logout(mock_db):
    database = sqlite3.connect(mock_db)
    shell = MiniProjectShell(database)
    assert not shell.login_session
    shell.login("bob@123.ca", "foo")
    assert shell.login_session
    shell.logout()
    assert not shell.login_session


def test_check_logged_in(mock_db):
    database = sqlite3.connect(mock_db)
    shell = MiniProjectShell(database)
    assert not shell.check_logged_in()
    assert not shell.login_session
    shell.login("bob@123.ca", "foo")
    assert shell.login_session
    assert shell.check_logged_in()
