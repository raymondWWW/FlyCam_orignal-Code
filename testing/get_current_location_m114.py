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

# TODO: get_current_location_manager_m114()


# Define function does_location_exist_m114(serial_string)
#   Searches serial string for "X:{}", "Y:{}", and "Z:{}"
#      Returns True if all 3 are found, else returns False



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

# Define call_m114() function that runs the M114 GCODE to the printer serial


def main():
    pass


main()

