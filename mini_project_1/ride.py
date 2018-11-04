import sqlite3
from datetime import datetime

from mini_project_1.loginsession import LoginSession

"""
Offer a ride.
The member should be able to offer rides by providing a date, the number of seats offered,
the price per seat, a luggage description, a source location, and a destination location.
The member should have the option of adding a car number and any set of enroute locations.

For locations (including source, destination and enroute), the member should be able to provide a keyword,
which can be a location code. If the keyword is not a location code, your system should return all locations
that have the keyword as a substring in city, province or address fields. If there are more than 5 matching locations,
at most 5 matches will be shown at a time, letting the member select a location or see more matches.
If a car number is entered, your system must ensure that the car belongs to the member.
Your system should automatically assign a unique ride number (rno) to the ride and set the member
as the driver of the ride.
"""


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
                if selection < len(items):
                    return selection
        elif index + 1 == len(items):
            selection = str(input("Enter selection number: "))

            if selection.isnumeric():
                selection = int(selection)
                if selection < len(items):
                    return selection
            index = -1
            print("An entry must be selected")
        index += 1


def get_location_id(dbcursor: sqlite3.Cursor, prompt: str = ""):
    """Gets a location lcode from the user."""
    print(prompt)
    keyword = str(input("Enter location keyword (exit to leave): "))

    if keyword == "exit":
        raise ConnectionAbortedError

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
        return get_selection(locations)[0]
    elif locations:
        return locations[0][0]
    else:
        print("No locations for %s" % keyword)
        raise LookupError


def get_date_from_user(prompt: str = 'Enter the date (YYYY-MM-DD): '):
    """ Gets and returns a date from the user """
    while 1:
        date = str(input(prompt))
        try:
            if date == "exit":
                raise ConnectionAbortedError("Could not get date")
            date = datetime.strptime(date, '%Y-%m-%d')
            return date
        except ValueError:
            print("Incorrect format")
    pass


def check_valid_cno(dbcursor: sqlite3.Cursor, cno: int, member: LoginSession):
    """ Returns whether a member has a car number cno in the database with cursor dbcursor"""
    dbcursor.execute("SELECT cno FROM cars WHERE cno = ? AND owner = ?", (cno, member.get_email()))
    if len(dbcursor.fetchall()):
        return True
    return False


def get_ride_offer_info(dbcursor: sqlite3.Cursor, member: LoginSession):
    date = num_of_seats = price_per_seat = luggage_desc = source = destination = None

    try:
        date = get_date_from_user()
    except ConnectionAbortedError:
        print("Aborting: You must give a date.")
        return

    try:
        while True:
            num_of_seats = int(input("Enter number of seats: "))
            if num_of_seats > 0:
                break
        while True:
            price_per_seat = int(input("Enter price per seat: "))
            if num_of_seats >= 0:
                price_per_seat
    except ValueError:
        print("Aborting: You must give a number")
        return

    luggage_desc = str(input("Enter luggage description: "))

    try:
        source = get_location_id(dbcursor, "Enter the ride source location: ")
        destination = get_location_id(dbcursor, "Enter the ride destination location: ")
    except ConnectionAbortedError:
        print("Aborting: You must give locations to offer a ride")
        return
    except LookupError:
        return

    enroute = set()

    while True:
        try:
            enroute.add(get_location_id(dbcursor, "Enter a enroute location: "))
        except ConnectionAbortedError:
            break
        except LookupError:
            print("No locations for that keyword")

    wants_to_add_cno = str(input("Do you want to add a car number? [y] or [n]")) == 'y'
    cno = None

    while wants_to_add_cno:
        try:
            cno = int(input("Enter a car number or exit: "))
            if check_valid_cno(dbcursor, cno, member):
                break
            print("You must give the car number of one of your cars")
        except ValueError:
            print("Please enter a number.")

    return date, num_of_seats, price_per_seat, luggage_desc, source, destination, cno, enroute


def offer_ride(database: sqlite3.Connection, member: LoginSession):
    """
    Tries to add a ride to the database for the member
    :return: if a ride has been added (True/False)
    """

    dbcursor = database.cursor()
    ride_offer_info = get_ride_offer_info(dbcursor, member)

    if ride_offer_info:
        date, seats, price, luggage, source, destination, cno, enroute = ride_offer_info

        dbcursor.execute("SELECT MAX(rno) FROM rides")
        rno = str(int(dbcursor.fetchone()[0]) + 1)

        # TODO: more error checking? sqlite3.OperationalError & sqlite3.IntegrityError
        dbcursor.execute(
            "INSERT INTO rides (rno, price, rdate, seats, lugDesc, src, dst, driver) VALUES " +
            "(?, ?, ?, ?, ?, ?, ?, ?)", (rno, price, date, seats, luggage, source, destination, member.get_email()))

        if cno:
            dbcursor.execute("UPDATE rides SET cno = ? WHERE rno = ?", (cno, rno))

        for place in enroute:
            dbcursor.execute("INSERT INTO enroute (rno, lcode) VALUES (?, ?)", (rno, place))

        database.commit()
        return True
    return False


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
