#!/usr/bin/python
# -*- coding: utf-8 -*-

"""pytests interacting with databases for mini-project-1"""
import os
import sqlite3
import pytest

DATABASE_DIR =os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'data',
    )

DATABASE_TABLE_CREATE = os.path.join(DATABASE_DIR, "create_tables.sql")
DATABASE_DATA_CREATE = os.path.join(DATABASE_DIR, "create_data.sql")


def create_test_db(filename: str):
    """Create a test database"""
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    # Create the tables
    cursor.executescript(open(DATABASE_TABLE_CREATE, "r").read())
    # Insert data
    cursor.executescript(open(DATABASE_DATA_CREATE, "r").read())
    # Save (commit) the changes
    conn.commit()


@pytest.fixture(scope="session")
def mock_db(tmpdir_factory):
    """pytest fixture returning the path to a mock database for testing"""
    filename = str(tmpdir_factory.mktemp("data").join("test.db"))
    create_test_db(filename)
    return filename


def test_example(mock_db):
    """Test example for interacting with data mocks"""
    conn = sqlite3.connect(mock_db)
    print(conn.execute("""SELECT name FROM members""").fetchall())
