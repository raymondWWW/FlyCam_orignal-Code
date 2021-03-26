# Generates location list based on starting location and well distance.

# Load Library
import yaml
import pandas as pd

# Load YAML File
# For now, dummy data
# sample_plate_specifications = {
#     "number_of_rows": 2,
#     "number_of_columns": 3,
#     "starting_location": (50, 140, 50),
#     "well_distance": (38, 38)
# }


# Generate location list
# Given the known starting location, number of rows, number of columns, and well distance (x and y)
# get the absolute position of all wells.
# Usage: A Matrix representing all well locations
def get_location_list(sample_plate_specifications):
    X = 0; Y = 1; Z = 2
    # print(sample_plate_specifications)
    number_of_rows = sample_plate_specifications["number_of_rows"]
    number_of_columns = sample_plate_specifications["number_of_columns"]
    starting_x = sample_plate_specifications["starting_location"][X]
    starting_y = sample_plate_specifications["starting_location"][Y]
    starting_z = sample_plate_specifications["starting_location"][Z]
    well_distance_x = sample_plate_specifications["well_distance"][X]
    well_distance_y = sample_plate_specifications["well_distance"][Y]
    number_of_wells = number_of_rows * number_of_columns

    # Create matrix of locations to match the actual well locations
    # TODO: Should I use NumPy?
    # Format (if a 2x3):
    #   [ (x, y, z), (x, y, z), (x, y, z)
    #     (x, y, z), (x, y, z), (x, y, z) ]
    # Or Maybe don't use tuples, use lists instead
    # TODO: Test how YAML saves tuples, if at all
    location_list = []

    # for loop that goes through each row
    for row_num in range(number_of_rows):
        # print("row_num", row_num)
        # Reset/set temp x
        temp_x = starting_x
        #   temp_y changes each iteration here (add a well_distance_y)
        temp_y = starting_y + (well_distance_y * row_num)
        #   temp_z stays the same throughout
        temp_z = starting_z
        # print("temp_x:", temp_x, "temp_y:", temp_y, "temp_z:", temp_z)

        # Create row
        location_list.append([])
        #   for loop that goes through each column
        for col_num in range(number_of_columns):
            # print("col_num:", col_num)
            #     temp_x changes each iteration here
            temp_x = starting_x + (well_distance_x * col_num)
            # print("temp_x:", temp_x, "temp_y:", temp_y, "temp_z:", temp_z)
            temp_location = [temp_x, temp_y, temp_z]
            location_list[row_num].append(temp_location)
        # print("Just finished a row")
        # print(location_list)
    return location_list

# Function: Create a path list of well locations based on sample plate specifications, then returns that list
# Usage: Exact locations to go to (then take pic or video)
def get_path_list(sample_plate_specifications):
    X = 0;
    Y = 1;
    Z = 2
    # print(sample_plate_specifications)
    number_of_rows = sample_plate_specifications["number_of_rows"]
    number_of_columns = sample_plate_specifications["number_of_columns"]
    starting_x = sample_plate_specifications["starting_location"][X]
    starting_y = sample_plate_specifications["starting_location"][Y]
    starting_z = sample_plate_specifications["starting_location"][Z]
    well_distance_x = sample_plate_specifications["well_distance"][X]
    well_distance_y = sample_plate_specifications["well_distance"][Y]
    number_of_wells = number_of_rows * number_of_columns

    # Create matrix of locations to match the actual well locations
    # TODO: Should I use NumPy?
    # Format (if a 2x3):
    #   [ (x, y, z), (x, y, z), (x, y, z)
    #     (x, y, z), (x, y, z), (x, y, z) ]
    # Or Maybe don't use tuples, use lists instead
    # TODO: Test how YAML saves tuples, if at all
    path_list = []

    # for loop that goes through each row
    for row_num in range(number_of_rows):
        # print("row_num", row_num)
        # Reset/set temp x
        temp_x = starting_x
        #   temp_y changes each iteration here (add a well_distance_y)
        temp_y = starting_y - (well_distance_y * row_num)
        #   temp_z stays the same throughout
        temp_z = starting_z
        # print("temp_x:", temp_x, "temp_y:", temp_y, "temp_z:", temp_z)

        # Create row
        # location_list.append([])
        #   for loop that goes through each column
        for col_num in range(number_of_columns):
            # print("col_num:", col_num)
            #     temp_x changes each iteration here
            temp_x = starting_x + (well_distance_x * col_num)
            # print("temp_x:", temp_x, "temp_y:", temp_y, "temp_z:", temp_z)
            temp_location = [temp_x, temp_y, temp_z]
            path_list.append(temp_location)
        # print("Just finished a row")
        # print(location_list)
    return path_list

# TODO: Create new function that saves to a PANDAS file instead.
# Function: Create a path list of well locations based on sample plate specifications, then returns that list
# Usage: Exact locations to go to (then take pic or video)
def get_path_dataframe(sample_plate_specifications):
    # Extract data from Sample Plate Specs, just like in the previous function

    # Create Empty Dataframe

    # Use for loop to go through each row
    #   Create temp variables for x, y, z
    #   Use for loop to go through each column
    #     change x as needed
    #     Create dataframe row using x, y, z
    #     Append new dataframe to original dataframe

    # return dataframe
    pass

def main():
    sample_plate_specifications = {
        "number_of_rows": 2,
        "number_of_columns": 3,
        "starting_location": [50, 140, 50],
        "well_distance": [38, 38]
    }

    # Start Location List Creation
    # location_list = get_location_list(sample_plate_specifications)
    # print(location_list)
    #
    # number_of_rows = sample_plate_specifications["number_of_rows"]
    # number_of_columns = sample_plate_specifications["number_of_columns"]
    #
    # # file name example: location_list_2x3_all.yaml
    # filename_yaml = "location_list_{}x{}_all.yaml".format(number_of_rows, number_of_columns)
    #
    # # dict_file = []
    # # TODO: Save a location as a Python List: [50, 178, 50] instead of something like this:
    # #   - - - 50
    # #       - 140
    # #       - 50
    # #     - - 88
    #
    # with open(filename_yaml, "w") as file:
    #     documents = yaml.dump(location_list, file)

    # Old Way, the YAML Way
    # Start Path List Creation
    # path_list = get_path_list(sample_plate_specifications)
    # print(path_list)

    # Save Path List to a YAML file
    # number_of_rows = sample_plate_specifications["number_of_rows"]
    # number_of_columns = sample_plate_specifications["number_of_columns"]
    #
    # # file name example: location_list_2x3_all.yaml
    # filename_yaml = "path_list_{}x{}_all.yaml".format(number_of_rows, number_of_columns)
    #
    # # dict_file = []
    # # TODO: Save to CSV File
    #
    # with open(filename_yaml, "w") as file:
    #     documents = yaml.dump(path_list, file)

    # New Way, the PANDAS/CSV way
    path_list = get_path_list(sample_plate_specifications)
    print(path_list)




main()

