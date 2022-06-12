"""
Algorithm Test for calculating well locations
using the centers of the corner wells of the well plates

Input number of rows and columns

Test 1, Row:
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


def main():
    print("Main")

    # Location format: location_dictionary = {"X": 0.00, "Y": 0.00, "Z": 0.00}

    # Placeholder data, row 1 start/end, number of rows and columns
    num_row = 3
    num_col = 5
    # Number of jumps to go from first well to last well, column-wise
    num_col_jump = num_col - 1

    X = "X"; Y = "Y"; Z = "Z"
    key_list = [X, Y, Z]

    # Row 1
    row_start = {"X": 1.00, "Y": 2.00, "Z": 3.00}
    row_end = {"X": 51.00, "Y": 3.00, "Z": 1.00}

    # Calculate location of each well in row using input number of columns

    # delta_x = abs(row_end[X] - row_start[X])
    # delta_y = abs(row_end[Y] - row_start[Y])
    # delta_z = abs(row_end[Z] - row_start[Z])
    # print(delta_z)

    delta_dict = {}
    for key in row_start.keys():
        # print(key)
        # delta_dict[key] = abs(row_end[key] - row_start[key])
        delta_dict[key] = row_end[key] - row_start[key]

    delta_x = delta_dict[X]
    print(f"delta_dict: {delta_dict}")
    print(f"delta_x: {delta_x}")

    # Difference between consecutive well centers, x direction
    # well_length_x = round(delta_x / num_col, 2)
    well_length_x = delta_x / num_col_jump
    x_step = delta_dict[X] / num_col_jump
    y_step = delta_dict[Y] / num_col_jump
    z_step = delta_dict[Z] / num_col_jump

    print(f"well_length_x: {well_length_x}")

    print(f"row_start: {row_start}")
    # Calculate well locations:
    # Index starts at 1, because these are physical well locations.
    for col in range(num_col):
        # print(col)
        # x_start = row_start[X]
        # y_start = row_start[Y]
        # z_start = row_start[Z]
        # x_loc = round(x_start + (x_step * col), 2)
        # y_loc = round(y_start + (y_step * col), 2)
        # z_loc = round(z_start + (z_step * col), 2)
        # print(f"col: {col}, x_loc: {x_loc}, y_loc: {y_loc}, z_loc: {z_loc}")

        # Loop Version, go through each key, calculate location
        well_loc = {}
        for key in row_start.keys():
            # print(key)
            start = row_start[key]
            step = delta_dict[key] / num_col_jump
            loc = round(start + (step * col), 2)
            well_loc[key] = loc

        print(f"col: {col+1}, {well_loc}")


    print(f"row_end: {row_end}")
    # Output those locations



    pass


if __name__ == "__main__":
    main()
