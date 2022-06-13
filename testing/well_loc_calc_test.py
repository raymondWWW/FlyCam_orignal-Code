"""
Algorithm Test for calculating well locations
using the centers of the corner wells of the well plates

Input number of rows and columns

Test 1, Row: [Done]
-Input first and last well location centers of row
-Calculate location of each well in row using input number of columns
-Output those locations

Test 2, Col:
-Input first and last well location centers of column
-Calculate location of each well in row using input number of rows
-Output those locations

Test 3, 4 Corners:
-Input 4 outer corners of well plate center locations
-Calculate location of each well in each row, save to dictionary
-Calculate location of each well in each col, save to dictionary
  -For dictionary, use row_col string index as key? or nested dictionary with row/col?
-Use loop to compare results, are they the same?
  -if they are within range of error, do an average?

Note:
- For all 3 tests, locations will have to rounded to 2 decimal places (e.g. 23.84895 is rounded to 23.85)
- Assumes Loc inputs are dictionary.

Ideas:
-GUI will create table length based on number of rows and columns
-Create GUI that will display editable table of well location?
-GUI that is an excel sheet, right side has "go to location button"?
-GUI that has clickable image to go to well location, and editable x/y/z?
-Save to CSV File
"""


def get_delta_dict(start_loc, end_loc):
    """
    Given two location dictionaries, get difference between them,
    return delta (or difference) dictionary. Assumes both dictionaries have
    the same keys.

    :param start_loc: A dictionary, format: {"X": 0.00, "Y": 0.00, "Z": 0.00}
    :param end_loc: A dictionary, format: {"X": 0.00, "Y": 0.00, "Z": 0.00}
    :return: A dictionary, delta dictionary, format: {"X": 0.00, "Y": 0.00, "Z": 0.00}
    """

    # Init empty dictionary
    delta_dict = {}

    # Use for loop to go through both keys of both dictionaries.
    for key in start_loc.keys():
        # Uncomment to print out key to make sure loop is working
        # print(key)

        # Calculate difference (or delta) between each X, Y, and Z
        delta_dict[key] = end_loc[key] - start_loc[key]

    # Uncomment to get print out delta_dict
    # print(f"delta_dict: {delta_dict}")
    return delta_dict


def get_row_locations(row_start, row_end, num_col):
    """
    Given the starting and ending row location, and number of columns,
    calculate each well's location in a row.

    TODO: Figure out if should return a dictionary using row/col as keys?

    :param row_start: A dictionary, format: {"X": 0.00, "Y": 0.00, "Z": 0.00}
    :param row_end: A dictionary, format: {"X": 0.00, "Y": 0.00, "Z": 0.00}
    :param num_col: An int, the number of columns in well plate
    :return: A list, list of well locations of a well
    """

    num_col_jump = num_col - 1

    # Get Step Distance Values
    # Maximum number of jumps to go from well 1 to last well.
    # Example: If there are 5 wells, you start at well 1.
    #          How many jumps does it take to go from well 1 to well 5?
    #          Answer 4, or number of columns - 1.
    # Used to calculate distance to jump to next well.
    max_col_jump = num_col - 1

    # Get Delta Dictionary,
    # used for calculating stepsize (or getting distance to jump to next well).
    delta_dict = get_delta_dict(row_start, row_end)

    # Initialize empty well_loc_list, to be appended later
    well_loc_list = []

    # print(f"row_start: {row_start}")
    # Calculate row well locations using number of columns
    for col in range(num_col):

        # Init empty dictionary well_loc
        well_loc = {}
        # Loop Version, go through each key (X, Y, or Z), calculate location
        for key in row_start.keys():
            # print(key)
            # Get Starting Location, as X, Y, or Z (individually)
            start = row_start[key]

            #  Get stepsize (in mm) amount to jump to next well
            step = delta_dict[key] / max_col_jump

            # Calculate actual location, round to two decimal places
            loc = round(start + (step * col), 2)

            # Add that location (float value) to that specific key (X, Y, or Z)
            well_loc[key] = loc

        # Print out location, make sure it increments correctly.
        # Prints out column number (index starts at 1 since physical well plates do that)
        # print(f"col: {col+1}, {well_loc}")

        # Append location to well_loc_list
        well_loc_list.append(well_loc)

    # Print out row_end location for comparison and debugging.
    # Last calculated row location (actual) should match row_end (expected)
    # print(f"row_end: {row_end}")

    # Output those locations
    # print(f"well_loc_list: {well_loc_list}")

    return well_loc_list


def main():
    # Location format: location_dictionary = {"X": 0.00, "Y": 0.00, "Z": 0.00}

    # Placeholder data, row 1 start/end, number of rows and columns
    num_row = 3
    num_col = 5

    X = "X"; Y = "Y"; Z = "Z"
    key_list = [X, Y, Z]

    # Row 1
    row_start = {"X": 1.00, "Y": 2.00, "Z": 3.00}
    row_end = {"X": 51.00, "Y": 3.00, "Z": 1.00}

    well_loc_list = get_row_locations(row_start, row_end, num_col)
    print(f"well_loc_list: {well_loc_list}")

    pass


if __name__ == "__main__":
    main()
