import sqlite3
from datetime import datetime

import pendulum

from mini_project_1.loginsession import LoginSession

"""
Offer a ride.
The member should be able to offer rides by providing a date, the number of seats offered,
the price per seat, a luggage description, a source location, and a destination location.
The member should have the option of adding a car number and any set of enroute locations.
"""


class ValueNotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)


def get_selection(items: list):
    """
    Gets the user to select a item from a list, displaying up to 5 items at a time.
    :param items: list of items
    :return: selected item from items
    """
    index = 0
    while True:
        print("%i: %s" % (index, items[index]))

        if index % 5 == 4:
            print("Press Enter to see more\n")
            selection = str(input("Enter selection number: "))

            if selection.isnumeric():
                selection = int(selection)
                if 0 < selection < len(items):
                    return items[selection]
            elif selection == "exit":
                return None
        elif index + 1 == len(items):
            print("Press Enter to return to the start of the list\n")
            selection = str(input("Enter selection number: "))

            if selection.isnumeric():
                selection = int(selection)
                if 0 < selection < len(items):
                    return items[selection]
            elif selection == "exit":
                return None
            index = -1
            print("An entry must be selected")
        index += 1


def get_location_id(dbcursor: sqlite3.Cursor, keyword: str, prompt:str = None):
    """Gets a location lcode from the user."""

    # get exact match locde
    dbcursor.execute(
        "SELECT * FROM locations WHERE lcode = ?", (keyword,))
    location = dbcursor.fetchall()
    if location:
        return location[0][0]

    # get matching locations, since it's not a lcode
    kw = '%' + keyword + '%'
    dbcursor.execute(
        "SELECT * FROM locations WHERE city LIKE ? OR prov LIKE ? OR address LIKE ?",
        (kw, kw, kw))
    locations = dbcursor.fetchall()

    # display and get user selection if more than one
    if len(locations) > 1:
        if prompt:
            print(prompt)
        return get_selection(locations)[0]
    elif locations:
        return locations[0][0]
    else:
        raise ValueNotFoundException("No location for "+keyword)


def check_valid_cno(dbcursor: sqlite3.Cursor, cno: int, member: LoginSession):
    """ Returns whether a member has a car number cno in the database with cursor dbcursor"""
    dbcursor.execute("SELECT cno FROM cars WHERE cno = ? AND owner = ?", (cno, member.get_email()))
    if len(dbcursor.fetchall()):
        return True
    return False


def offer_ride(database: sqlite3.Connection, member: LoginSession, date: pendulum.DateTime, seats: int,
               price: int, luggage: str, source: str, destination: str, cno: str = None, enroute: set = set()):
    """
    Tries to add a ride to the database for the member
    :return: if a ride has been added (True/False)
    """
    dbcursor = database.cursor()
    dbcursor.execute("SELECT MAX(rno) FROM rides")
    rno = str(int(dbcursor.fetchone()[0]) + 1)
    print(rno, price, date, seats, luggage, source, destination, member.get_email())
    print(cno)
    print(enroute)

    try:
        dbcursor.execute(
            "INSERT INTO rides (rno, price, rdate, seats, lugDesc, src, dst, driver) VALUES " +
            "(?, ?, ?, ?, ?, ?, ?, ?)", (rno, price, date, seats, luggage, source, destination, member.get_email()))

        if cno:
            dbcursor.execute("UPDATE rides SET cno = ? WHERE rno = ?", (cno, rno))

        for place in enroute:
            dbcursor.execute("INSERT INTO enroute (rno, lcode) VALUES (?, ?)", (rno, place))
    except sqlite3.OperationalError as e:
        print(e)
        return False
    except sqlite3.IntegrityError as e:
        print(e)
        return False

    database.commit()
    return True


"""
Search for rides.
The member should be able to enter 1-3 location keywords and retrieve all rides that match all keywords. 
A ride matches a keyword if the keyword matches one of the locations source, destination, or enroute. 
Also a location matches a keyword if the keyword is either the location code or a substring of the city, 
the province, or the address fields of the location. For each matching ride, all information about the ride 
(from the rides table) and car details (if any) will be displayed. If there are more than 5 matches, 
at most 5 will be shown at a time, and the member is provided an option to see more. 
The member should be able to select a ride and message the member posting the ride that h/she 
wants to book seats on that ride.
"""


def search_for_ride():
    """Search for rides"""
    pass


"""
Book members or cancel bookings.
The member should be able to list all bookings on rides s/he offers and cancel any booking. 
For any booking that is cancelled (i.e. being deleted from the booking table), 
a proper message should be sent to the member whose booking is cancelled. 
Also the member should be able to book other members on the rides they offer. 
Your system should list all rides the member offers with the number of available seats for each ride 
(i.e., seats that are not booked). If there are more than 5 matching rides, at most 5 will be shown at a time, 
and the member will have the option to see more. The member should be able to select a ride and book a member for 
that ride by entering the member email, the number of seats booked, the cost per seat, 
and pickup and drop off location codes. Your system should assign a unique booking number (bno) to the booking. 
Your system should give a warning if a ride is being overbooked (i.e. the number of seats booked exceeds the number 
of seats offered), but will allow overbooking if the member confirms it. After a successful booking, 
a proper message should be sent to the other member that s/he is booked on the ride.
Post ride requests.The member should be able to post a ride request by providing a date, a pick up location code, 
a drop off location code, and the amount willing to pay per seat. The request rid is set by your system to a unique 
number and the email is set to the email address of the member.
"""


def book_member():
    """Book members"""
    pass


"""
Search and delete ride requests. 
The member should be able to see all his/her ride requests and be able to delete any of them. 
Also the member should be able to provide a location code or a city and see a listing of all requests with a 
pickup location matching the location code or the city entered. If there are more than 5 matches, at most 5 matches
 will be shown at a time. The member should be able to select a request and message the posting member, for example 
 asking the member to check out a ride.
"""

if __name__ == "__main__":
    conn = sqlite3.connect("test2.db")
    test_dbcursor = conn.cursor()

    # test_dbcursor.executescript(open("data/create_tables.sql", "r").read())
    # test_dbcursor.executescript(open("data/create_data.sql", "r").read())
    # conn.commit()
    test_dbcursor.execute(
        "SELECT * FROM rides Where rno > 42")

    edm_location = test_dbcursor.fetchall()
    print(edm_location)
    test_dbcursor.execute(
        "SELECT * FROM enroute Where rno > 42")

    edm_location = test_dbcursor.fetchall()
    print(edm_location)
    print("-----------------")
    try:
        offer_ride(conn, LoginSession("jane_doe@abc.ca", "passyW"))
    except LookupError:
        pass
    except ConnectionAbortedError:
        pass

    test_dbcursor.execute(
        "SELECT * FROM rides Where rno > 42")

    edm_location = test_dbcursor.fetchall()
    print(edm_location)
    test_dbcursor.execute(
        "SELECT * FROM enroute Where rno > 42")

    edm_location = test_dbcursor.fetchall()
    print(edm_location)

    test_dbcursor.close()
    # conn.commit()
    conn.close()  # <--- Close the connection..
