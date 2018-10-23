#!/usr/bin/python
# -*- coding: utf-8 -*-

"""pytests interacting with databases for mini-project-1"""

import sqlite3
import pytest


def create_test_db(filename: str):
    """Create a test database"""
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    # Create the tables
    cursor.executescript(open("../create_tables.sql", "r").read())
    # Insert data
    cursor.executescript(open("../test_data.sql", "r").read())
    # Save (commit) the changes
    conn.commit()


@pytest.fixture(scope="session")
def mock_db(tmpdir_factory):
    """pytest fixture returning the path to a mock database for testing"""
    filename = str(tmpdir_factory.mktemp("data").join("test.db"))
    create_test_db(filename)
    return filename


def test_example(mock_db):
    """Test example for interacting with database mocks"""
    conn = sqlite3.connect(mock_db)
    print(conn.execute("""SELECT name FROM members""").fetchall())
