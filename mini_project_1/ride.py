#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3

import pendulum

from mini_project_1.loginsession import LoginSession

"""Book members or cancel bookings.

The member should be able to list all bookings on rides s/he offers and 
cancel any booking. For any booking that is cancelled (i.e. being deleted 
from the booking table), a proper message should be sent to the member whose 
booking is cancelled. Also the member should be able to book other members 
on the rides they offer. Your system should list all rides the member offers 
with the number of available seats for each ride (i.e., seats that are not 
booked). If there are more than 5 matching rides, at most 5 will be shown at 
a time, and the member will have the option to see more. The member should 
be able to select a ride and book a member for that ride by entering the 
member email, the number of seats booked, the cost per seat, and pickup and 
drop off location codes. Your system should assign a unique booking number (
bno) to the booking. Your system should give a warning if a ride is being 
overbooked (i.e. the number of seats booked exceeds the number of seats 
offered), but will allow overbooking if the member confirms it. After a 
successful booking, a proper message should be sent to the other member that 
s/he is booked on the ride. Post ride requests.The member should be able to 
post a ride request by providing a date, a pick up location code, a drop off 
location code, and the amount willing to pay per seat. The request rid is 
set by your system to a unique number and the email is set to the email 
address of the member.
"""


def book_member():
    """Book members"""
    pass
