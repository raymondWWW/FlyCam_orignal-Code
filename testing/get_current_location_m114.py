"""
Helper Functions for the "Current Location Manager" 3D printer Gcode M114,
searches string for current location,
parses string for current location
Author: Johnny Duong
Date: 1 Apr 2021


Possible Future Updates:
-Requires separate printer serial connection module created, then this module will have manager function.


Things to think about:
-Not using the Parse library, create functions that search for the variable, gets digits afterwards until a non-digit
 or period is found
"""

# import parse library
from parse import search

# CONSTANTS
KEYWORD_SEARCH = "X:{:.2f}"

# TODO: get_current_location_manager_m114()


# Define function does_location_exist_m114(serial_string)
#   Searches serial string for "X:{}", "Y:{}", and "Z:{}"
#      Returns True if all 3 are found, else returns False
def does_location_exist_m114(serial_string):
    # Intialize is_location_found as False, this will be returned
    is_location_found = False

    # TODO: Figure out how to search all 3 Coordinates, maybe a list of generic function?

    # Using Parse Library, search for the X Keyword in serial_string
    search_result = search(KEYWORD_SEARCH, serial_string)

    # If None is not found, set is_location_found to True, otherwise it is false.
    if search_result is not None:
        is_location_found = True

    # return is_location_found
    return is_location_found



# Define function parse_m114(serial_string)
#   Uses findall to get all incidents of" X:{}", "Y:{}", and "Z:{}",
#     then uses last result (this is usually the current location).
#     Returns current_location_dictionary and boolean (True if successful, False if current location could not be parsed or found)
# Algorithm:
#  Initialize current_location_dictionary with placeholder values (zero) for x, y, z
#  Initialize isLocationFound with False
#  Use findall to find all incidents of "X:{}", store into search_results_x variable
#  Use findall to find all incidents of "Y:{}", store into search_results_y variable
#  Use findall to find all incidents of "Z:{}", store into search_results_z variable

#  Initialize counter variable, temp_x (for storing the x value found,
#    to be put into the current_location_dictionary later)
#  Use a for loop to go through all of search_results_x
#    store results into temp_x
#    increment counter
#  if counter is zero, isLocationFound = False
#  if counter is 1+, the last search result should be current location. TODO: Test if this is true.

# Repeat the above, now with y and z. TODO: Consider creating a function that does the above

# Return current_location_dictionary and isLocationFound

# TODO: Use a search_keywords list to automate the usage of findall.



# Future Functions:
# Define Manager Function that calls the above 2 functions and interacts with printer module

# Define call_m114() function that runs the M114 GCODE to the printer serial connection


def main():
    # serial_string = "X:1.45Y:2.67Z:100.09E:3.00 Count X: 4.00Y:5.00Z:102.00\nok"
    # serial_string = "wait\nwait\nok\nX:1.23 Y:3.45 Z:5.678 E:0.0000"
    serial_string = "blah"

    is_location_found = does_location_exist_m114(serial_string)
    print("is_location_found:", is_location_found)

    pass


main()

