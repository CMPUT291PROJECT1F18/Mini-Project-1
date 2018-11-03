import sqlite3
from datetime import datetime

from mini_project_1.member import Member

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


def get_selection(items):
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
        elif index+1 == len(items):
            selection = str(input("Enter selection number: "))

            if selection.isnumeric():
                selection = int(selection)
                if selection < len(items):
                    return selection
            index = -1
            print("An entry must be selected")
        index += 1


def get_location(dbcursor: sqlite3.Cursor, filter: str = None):
    """Gets a location from the user."""
    while True:
        keyword = str(input("Enter a location keyword (exit to leave): "))

        if keyword == "exit":
            raise ConnectionAbortedError

        # get matching locations
        dbcursor.execute(
            "SELECT * FROM locations WHERE lcode = ?", (keyword,))
        location = dbcursor.fetchall()
        if location:
            return location

        # not a lcode --> see if its a substring of city, province or address
        keyword = '%' + keyword + '%' # set keyword to be any string with keyword in it
        dbcursor.execute(
            "SELECT * FROM locations WHERE city LIKE ? OR prov LIKE ? OR address LIKE ?",
            (keyword, keyword, keyword))
        locations = dbcursor.fetchall()

        # display and get user selection if more than one
        if len(locations) > 1:
            return get_selection(locations)
        elif locations:
            return locations
        else:
            print("No locations for %s" %keyword)
            raise LookupError


def get_date_from_user(prompt: str = 'Enter the date (YYYY-MM-DD): '):
    """
    Gets and returns a date from the user
    :param prompt:
    :return:
    """
    while 1:
        date = str(input(prompt))
        try:
            if date == "exit":
                raise LookupError("Could not get date")
            date = datetime.strptime(date, '%Y-%m-%d')
            return date
        except ValueError:
            print("Incorrect format")
    pass


def offer_ride(dbcursor: sqlite3.Cursor, member: Member):
    """

    :param dbcursor:
    :param member:
    :return:
    """
    try:
        date = get_date_from_user()
    except LookupError:
        return
    try:
        num_of_seats = int(input("Enter number of seats: "))
        price_per_seat = int(input("Enter price per seat: "))
    except ValueError:
        print("Must give numbers")

    luggage_desc = str(input("Luggage description: "))

    try:
        source = get_location(dbcursor)
        dest = get_location(dbcursor)
    except ConnectionAbortedError:
        print("You must give locations to offer a ride")
    except LookupError:
        print("No locations")
    pass


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
    """"""
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


def search_for_ride():
    """"""
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
    dbcursor = conn.cursor()

    dbcursor.executescript(open("data/create_tables.sql", "r").read())
    dbcursor.executescript(open("data/create_data.sql", "r").read())
    conn.commit()
    dbcursor.execute(
        "SELECT * FROM locations Where city like '%Edm%'")

    location = dbcursor.fetchall()
    print(location)
    print("-----------------")
    try:
        get_location(dbcursor)
        get_location(dbcursor)
        get_location(dbcursor)
    except LookupError:
        pass

    dbcursor.close()
    conn.close()  # <--- Close the connection..