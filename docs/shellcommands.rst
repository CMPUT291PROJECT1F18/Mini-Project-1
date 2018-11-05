#################################
MiniProjectShell Command Line Use
#################################

Below is usage documentation on using the mini-project-1 shell and
the various commands associated with it.

book_member
===========

.. argparse::
   :module: mini_project_1.book_member
   :func: get_book_member_parser
   :prog: book_member


cancel_booking
==============

.. argparse::
   :module: mini_project_1.cancel_booking
   :func: get_cancel_booking_parser
   :prog: cancel_booking


delete_request
==============

.. argparse::
   :module: mini_project_1.delete_request
   :func: get_delete_request_parser
   :prog: delete_request


.. argparse::
   :module: mini_project_1.list_bookings
   :func: get_list_bookings_parser
   :prog: list_bookings


list_requests
=============

.. argparse::
   :module: mini_project_1.list_requests
   :func: get_list_ride_requests_parser
   :prog: list_requests


logout
======

.. argparse::
   :module: mini_project_1.logout
   :func: get_logout_parser
   :prog: logout


offer_ride
==========

.. argparse::
   :module: mini_project_1.offer_ride
   :func: get_offer_ride_parser
   :prog: offer_ride


post_request
============

.. argparse::
   :module: mini_project_1.post_request
   :func: get_post_request_parser
   :prog: post_request


search_requests_lcode
=====================

.. argparse::
   :module: mini_project_1.search_requests
   :func: get_search_requests_lcode_parser
   :prog: search_requests_lcode


search_requests_city
====================

.. argparse::
   :module: mini_project_1.search_requests
   :func: get_search_requests_city_parser
   :prog: search_requests_city


search_rides
============

.. argparse::
   :module: mini_project_1.search_rides
   :func: get_search_for_ride_parser
   :prog: search_rides


select_request
==============

.. argparse::
   :module: mini_project_1.select_request
   :func: get_select_request_parser
   :prog: select_request


show_inbox
==========

.. argparse::
   :module: mini_project_1.show_inbox
   :func: get_show_inbox_parser
   :prog: show_inbox


login
=====

Login to the mini-project-1 database.

.. code-block:: bash

    usage: login


register
========

Register a new member to the mini-project-1 database.

.. code-block:: bash

    usage: register


exit
====

Logout (if needed) and exit out of the mini-project-1 shell.

.. code-block:: bash

    usage: exit



